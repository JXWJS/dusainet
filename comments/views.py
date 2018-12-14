from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from notifications.signals import notify

from .models import Comment, ReadBookComment
from .forms import CommentForm, ReadBookCommentForm

from article.models import ArticlesPost
from readbook.models import ReadBook

from utils.utils import send_email_to_user

from django.views.generic import CreateView
from braces.views import LoginRequiredMixin


# Create your views here.


class CommentCreateView(LoginRequiredMixin,
                        CreateView):
    """
    发布博文、读书的新评论的视图
    可处理get或post请求
    """
    fields = [
        'body',
    ]

    def get_article_and_commentform(self, request, article_id):
        """
        获取回复的文章种类、绑定的评论表单
        """
        if request.POST['article_type'] == 'article':
            article = get_object_or_404(ArticlesPost, id=article_id)
            comment_form = CommentForm(request.POST)
        elif request.POST['article_type'] == 'readbook':
            article = get_object_or_404(ReadBook, id=article_id)
            comment_form = ReadBookCommentForm(request.POST)
        else:
            article = None
            comment_form = None
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
            comment_form = None
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
            parent_comment = None
        return parent_comment

    def get_template(self, article_type):
        if article_type == 'article':
            template = 'comments/reply_post_comment.html'
        elif article_type == 'readbook':
            template = 'comments/read_book_reply_post_comment.html'
        else:
            template = None
        return template

    def get(self, request, *args, **kwargs):
        """
        处理get请求
        """
        article_id = kwargs.get('article_id')
        node_id = kwargs.get('node_id')
        article_type = kwargs.get('article_type')
        comment_form = self.get_comment_form(article_type)
        comment = self.get_parent_comment(article_type, node_id)
        template = self.get_template(article_type)

        return render(
            request,
            template,
            {'comment_form': comment_form,
             'article_id': article_id,
             'node_id': node_id,
             'comment': comment,
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

        # 创建新评论
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            article_type = request.POST['article_type']

            # 对二级评论，赋值root节点的id
            if self.kwargs.get('node_id'):
                node_id = kwargs.get('node_id')
                # print(node_id)

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
        return redirect(article)