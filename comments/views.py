from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from notifications.signals import notify

from .models import (
    Comment,
    ReadBookComment,
    VlogComment,
)

from .forms import (
    CommentForm,
    ReadBookCommentForm,
    VlogCommentForm,
)

from article.models import ArticlesPost
from readbook.models import ReadBook
from vlog.models import Vlog

from utils.utils import send_email_to_user

from django.views.generic import CreateView, UpdateView
from braces.views import LoginRequiredMixin


class CommentUpdateView(LoginRequiredMixin,
                        UpdateView):
    """
    更新回复
    """
    context_object_name = 'comment'
    template_name = 'comments/edit.html'
    fields = ['body']
    login_url = "/accounts/weibo/login/?process=login"

    def dispatch(self, request, *args, **kwargs):
        """初始化"""
        self.article_type = self.request.GET.get('article_type')
        return super(CommentUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # 禁止编辑已删除的comment
        if self.object.is_deleted:
            raise PermissionDenied

        # 初始化旧正文
        context = super().get_context_data(**kwargs)
        ini = {'body': self.object.body}
        if self.article_type == 'article':
            comment_form = CommentForm(initial=ini)
        elif self.article_type == 'readbook':
            comment_form = ReadBookCommentForm(initial=ini)
        else:
            comment_form = VlogCommentForm(initial=ini)
        data = {
            'comment_form': comment_form
        }
        context.update(data)
        return context

    def get_queryset(self):
        """获取 models"""
        if self.article_type == 'article':
            queryset = Comment.objects.all()
        elif self.article_type == 'readbook':
            queryset = ReadBookComment.objects.all()
        else:
            queryset = VlogComment.objects.all()
        return queryset

    def form_valid(self, form):
        """鉴权"""
        if self.request.user != self.object.user and not self.request.user.is_staff:
            raise PermissionDenied
        return super(CommentUpdateView, self).form_valid(form)

    def get_success_url(self):
        """获取重定向url"""
        obj = self.get_object()
        redirect_url = obj.article.get_absolute_url() + '#F' + str(obj.id)
        return redirect_url

    def post(self, request, *args, **kwargs):
        # 暂时用这种方法来检查空值，需优化
        if request.POST['body'] == '':
            self.get(request, *args, **kwargs)
        return super(CommentUpdateView, self).post(request, *args, **kwargs)


@login_required(login_url='/accounts/weibo/login/?process=login')
def comment_soft_delete(request):
    """
    软删除回复
    本人及管理员可操作
    """
    comment_id = request.GET.get('comment_id')

    # get model
    article_type = request.GET.get('article_type')
    if article_type == 'article':
        comment = get_object_or_404(Comment, id=comment_id)
    elif article_type == 'readbook':
        comment = get_object_or_404(ReadBookComment, id=comment_id)
    else:
        comment = get_object_or_404(VlogComment, id=comment_id)

    # 鉴权
    if request.user != comment.user and not request.user.is_staff:
        raise PermissionDenied

    # 添加删除标记
    if request.user.is_staff:
        comment.is_deleted_by_staff = True
    comment.is_deleted = True
    comment.save()

    redirect_url = comment.article.get_absolute_url() + '#F' + str(comment.id)
    return redirect(redirect_url)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    发布博文、读书、vlog 的新评论的视图
    可处理get或post请求
    model设计问题导致代码臃肿
    """
    login_url = "/accounts/weibo/login/?process=login"
    fields = [
        'body',
    ]

    def get_article_and_commentform(self, request, article_id):
        """
        获取: 回复的文章种类、绑定的评论表单
        """
        if request.POST['article_type'] == 'article':
            article = get_object_or_404(ArticlesPost, id=article_id)
            comment_form = CommentForm(request.POST)
        elif request.POST['article_type'] == 'readbook':
            article = get_object_or_404(ReadBook, id=article_id)
            comment_form = ReadBookCommentForm(request.POST)
        else:
            article = get_object_or_404(Vlog, id=article_id)
            comment_form = VlogCommentForm(request.POST)
        return (article, comment_form)

    def get_comment_form(self, article_type):
        """
        获取未绑定的评论表单
        """
        if article_type == 'article':
            comment_form = CommentForm()
        elif article_type == 'readbook':
            comment_form = ReadBookCommentForm()
        else:
            comment_form = VlogCommentForm()
        return comment_form

    def get_parent_comment(self, article_type, node_id):
        """
        获取二级回复的父级回复
        """
        if article_type == 'article':
            parent_comment = Comment.objects.get(id=node_id)
        elif article_type == 'readbook':
            parent_comment = ReadBookComment.objects.get(id=node_id)
        else:
            parent_comment = VlogComment.objects.get(id=node_id)
        return parent_comment

    def get(self, request, *args, **kwargs):
        """
        处理get请求
        """
        article_id = kwargs.get('article_id')
        node_id = kwargs.get('node_id')
        article_type = kwargs.get('article_type')

        comment_form = self.get_comment_form(article_type)
        comment = self.get_parent_comment(article_type, node_id)

        template = 'comments/reply_post_comment.html'

        return render(
            request,
            template,
            {'comment_form': comment_form,
             'article_id': article_id,
             'node_id': node_id,
             'comment': comment,
             'article_type': article_type,
             }
        )

    def post(self, request, *args, **kwargs):
        """
        处理post请求
        """
        article, comment_form = self.get_article_and_commentform(
            request,
            self.kwargs.get('article_id')
        )

        # 暂时用这种方法来检查空值，需优化
        if request.POST['body'] == '':
            return redirect(article)

        # 创建新评论
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            article_type = request.POST['article_type']

            # 对二级评论，赋值root节点的id
            if self.kwargs.get('node_id'):
                node_id = kwargs.get('node_id')

                # 判断回复属于博文、读书或视频
                # 并赋值父级评论
                parent_comment = self.get_parent_comment(article_type, node_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user

                # 对不是staff的父级评论发送通知
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        description=article_type,
                        action_object=new_comment,
                    )
            else:
                new_comment.reply_to = None

            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()

            # 给staff发送通知
            notify.send(
                request.user,
                recipient=User.objects.filter(is_staff=1),
                verb='回复了你',
                target=article,
                description=article_type,
                action_object=new_comment,
            )

            # 给博主发送通知邮件
            # send_email_to_user(recipient='dusaiphoto@foxmail.com')

        # 输入不合法
        else:
            raise PermissionDenied

        redirect_url = article.get_absolute_url() + '#F' + str(new_comment.id)
        return redirect(redirect_url)
