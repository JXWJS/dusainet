from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import ArticlesPost, ArticlesColumn
from .forms import ArticleCreateForm

from comments.models import Comment
from comments.forms import CommentForm
from course.models import Course

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin


# Create your views here.

# 文章列表Mixin
class ArticleMixin:
    model = ArticlesPost
    context_object_name = 'articles'
    template_name = 'article/article_list.html'


# 所有文章
class ArticlePostView(ArticleMixin, ListView):
    pass


# 栏目文章
class ArticlePostByColumnView(ArticleMixin, ListView):
    template_name = 'article/article_list_by_column.html'

    def get_queryset(self):
        qs = super(ArticlePostByColumnView, self).get_queryset()
        return qs.filter(column=self.kwargs['column_id'])


# 标签文章
class ArticlePostByTagView(ArticleMixin, ListView):
    def get_queryset(self):
        qs = super(ArticlePostByTagView, self).get_queryset()
        return qs.filter(tags__name__in=[self.kwargs['tag_name']]).order_by('-total_views')


class ArticlePostByMostViewedView(ArticleMixin, ListView):
    def get_queryset(self):
        qs = super(ArticlePostByMostViewedView, self).get_queryset()
        if 'column_id' in self.kwargs:
            self.template_name = 'article/article_list_by_column.html'
            return qs.filter(column=self.kwargs['column_id']).order_by('-total_views')
        else:
            return qs.order_by('-total_views')


# 文章内容
def article_detail(request, article_id):
    article = ArticlesPost.objects.get(id=article_id)
    article.total_views = article.total_views
    article.increase_views()

    # 评论
    comment_form = CommentForm()

    # 取出教程中前一条和后一条文章
    if article.course:
        next_article = ArticlesPost.objects.filter(course_sequence__gt=article.course_sequence).order_by('course_sequence')
        pre_article = ArticlesPost.objects.filter(course_sequence__lt=article.course_sequence).order_by('-course_sequence')

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
    else:
        context = {'article': article,
                   'comment_form': comment_form,
                   # 生成树形评论
                   'comments': Comment.objects.filter(article_id=article_id),
                   }
        return render(request, 'article/article_detail.html', context=context)


# 发表文章
class ArticleCreateView(LoginRequiredMixin, SuperuserRequiredMixin, ArticleMixin, CreateView):
    fields = ['title', 'column', 'tags', 'body', 'url', 'course', 'course_sequence']
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


# 更新文章
class ArticleUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, ArticleMixin, UpdateView):
    success_url = reverse_lazy("article:article_list")
    context_object_name = 'article'
    template_name = 'article/article_create.html'
    fields = ['title', 'column', 'tags', 'body']
