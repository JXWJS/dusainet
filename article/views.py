from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import ArticlesPost, ArticlesColumn
from .forms import ArticleCreateForm

from comments.models import Comment
from comments.forms import CommentForm
from utils.utils import PaginatorMixin

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin


# Create your views here.

class ArticleMixin(PaginatorMixin):
    """
    文章Mixin
    """
    model = ArticlesPost
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = ArticlesColumn.objects.all()
        data = {
            'columns': columns
        }
        context.update(data)
        return context


# 文章列表
class ArticlePostView(ArticleMixin, ListView):
    template_name = 'article/article_list.html'

    def dispatch(self, request, *args, **kwargs):
        """
        init
        """
        self.column_id = self.request.GET.get('column_id')
        self.order = self.request.GET.get('order')
        self.tag = self.request.GET.get('tag')

        # call the view
        return super(ArticlePostView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        获取模型数组
        :return: queryset
        """

        queryset = super(ArticlePostView, self).get_queryset()
        if self.column_id:
            queryset = queryset.filter(column=self.column_id)

        if self.order == 'total_views':
            queryset = queryset.order_by('-total_views')

        if self.tag:
            queryset = queryset.filter(tags__name__in=[self.tag])
            print(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        """
        获取上下文
        :return: context
        """

        context = super(ArticlePostView, self).get_context_data(**kwargs)

        # 更新栏目信息
        if self.column_id:
            c_data = {
                'column_id': int(self.column_id),
            }
            context.update(c_data)
        # 更新排序信息
        if self.order:
            o_data = {
                'order': self.order
            }
            context.update(o_data)
        # 更新标签信息
        if self.tag:
            t_data = {
                'tag': self.tag
            }
            context.update(t_data)
        return context


def article_detail(request, article_id):
    """
    文章详情的view
    :param article_id: 文章的id
    """
    article = ArticlesPost.objects.get(id=article_id)
    article.increase_views()

    # 传递给模板文章类型，用于评论表单区分
    article_type = 'article'

    # 评论
    comment_form = CommentForm()

    # 根据教程序号，取出教程中前一条和后一条文章
    if article.course:
        next_article = ArticlesPost.objects.filter(
            course_sequence__gt=article.course_sequence,
            course=article.course,
        ).order_by('course_sequence')

        pre_article = ArticlesPost.objects.filter(
            course_sequence__lt=article.course_sequence,
            course=article.course
        ).order_by('-course_sequence')

        if pre_article.count() > 0:
            pre_article = pre_article[0]
        else:
            pre_article = None

        if next_article.count() > 0:
            next_article = next_article[0]
        else:
            next_article = None

        course_articles = article.course.article.all().order_by('course_sequence')

        context = {'article': article,
                   'comment_form': comment_form,
                   # 生成树形评论
                   'comments': Comment.objects.filter(article_id=article_id),
                   'course_articles': course_articles,
                   'pre_article': pre_article,
                   'next_article': next_article,
                   'article_type': article_type,
                   }

        return render(request, 'course/article_detail.html', context=context)
    # 文章不属于任何教程
    else:
        context = {'article': article,
                   'comment_form': comment_form,
                   # 生成树形评论
                   'comments': Comment.objects.filter(article_id=article_id),
                   'article_type': article_type,
                   }
        return render(request, 'article/article_detail.html', context=context)


# 发表文章
class ArticleCreateView(LoginRequiredMixin,
                        StaffuserRequiredMixin,
                        ArticleMixin,
                        CreateView):
    fields = [
        'title',
        'column',
        'tags',
        'body',
        'url',
        'course',
        'course_sequence',
    ]

    template_name = 'article/article_create.html'

    def post(self, request, *args, **kwargs):
        forms = ArticleCreateForm(data=request.POST)
        if forms.is_valid():
            new_article = forms.save(commit=False)
            new_article.author = self.request.user
            new_article.save()

            # Without this next line the tags won't be saved.
            forms.save_m2m()

            return redirect("article:article_list")
        return self.render_to_response({"forms": forms})


class ArticleUpdateView(LoginRequiredMixin,
                        StaffuserRequiredMixin,
                        ArticleMixin,
                        UpdateView):
    """
    更新文章
    废弃，暂用admin代替
    """
    success_url = reverse_lazy("article:article_list")
    context_object_name = 'article'
    template_name = 'article/article_create.html'
    fields = ['title', 'column', 'tags', 'body']
