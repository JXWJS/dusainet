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
    template_name = 'article/article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = ArticlesColumn.objects.all()
        data = {
            'columns': columns
        }
        context.update(data)
        return context


# 所有文章的list
class ArticlePostView(ArticleMixin, ListView):

    def get_queryset(self):
        """
        获取模型数组
        :return: queryset
        """
        column_id = self.request.GET.get('column_id')
        order = self.request.GET.get('order')

        queryset = super(ArticlePostView, self).get_queryset()
        if column_id:
            queryset = queryset.filter(column=column_id)

        if order == 'total_views':
            queryset = queryset.order_by('-total_views')

        return queryset

    def get_context_data(self, **kwargs):
        """
        获取上下文
        :return: context
        """
        column_id = self.request.GET.get('column_id')
        order = self.request.GET.get('order')

        context = super(ArticlePostView, self).get_context_data(**kwargs)

        # 更新栏目信息
        if column_id:
            c_data = {
                'column_id': int(column_id),
            }
            context.update(c_data)
        # 更新排序信息
        if order:
            o_data = {
                'order': order
            }
            context.update(o_data)
        return context


class ArticlePostByColumnView(ArticleMixin, ListView):
    """
    栏目文章list
    """

    def get_context_data(self, **kwargs):
        """
        添加is_list_by_column上下文标记
        若标记为true
        模板显示栏目最热文章
        false则显示综合最热文章
        :param kwargs:
        :return: 上下文对象
        """
        context = super(ArticlePostByColumnView, self).get_context_data(**kwargs)
        is_list_by_column = True
        data = {
            'is_list_by_column': is_list_by_column
        }
        context.update(data)
        return context

    def get_queryset(self):
        """
        :return: 栏目的qs
        """
        qs = super(ArticlePostByColumnView, self).get_queryset()
        return qs.filter(column=self.kwargs['column_id'])


class ArticlePostByTagView(ArticleMixin, ListView):
    """
    根据标签检索文章
    按热度排序
    """

    def get_queryset(self):
        qs = super(ArticlePostByTagView, self).get_queryset()
        return qs.filter(tags__name__in=[self.kwargs['tag_name']]).order_by('-total_views')


class ArticlePostByMostViewedView(ArticleMixin, ListView):
    """
    按浏览数排序的list
    """

    def get_context_data(self, **kwargs):
        """
        如果模板传入了column_id
        则添加is_list_by_column标记
        :return: context上下文
        """
        context = super(ArticlePostByMostViewedView, self).get_context_data(**kwargs)
        if 'column_id' in self.kwargs:
            is_list_by_column = True
            data = {
                'is_list_by_column': is_list_by_column
            }
            context.update(data)
        return context

    def get_queryset(self):
        """
        如果is_list_by_column为true
        则在栏目中检索
        否则检索所有文章
        :return: qs
        """
        qs = super(ArticlePostByMostViewedView, self).get_queryset()
        if 'column_id' in self.kwargs:
            self.template_name = 'article/article_list.html'
            return qs.filter(column=self.kwargs['column_id']).order_by('-total_views')
        else:
            return qs.order_by('-total_views')


def article_detail(request, article_id):
    """
    文章详情的view
    :param article_id: 文章的id
    """
    article = ArticlesPost.objects.get(id=article_id)
    article.total_views = article.total_views
    article.increase_views()

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
                   }

        return render(request, 'course/article_detail.html', context=context)
    # 文章不属于任何教程
    else:
        context = {'article': article,
                   'comment_form': comment_form,
                   # 生成树形评论
                   'comments': Comment.objects.filter(article_id=article_id),
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
