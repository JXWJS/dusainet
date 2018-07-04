from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect

from .models import ArticlesPost
from .forms import ArticleCreateForm

from comments.models import Comment
from comments.forms import CommentForm

from braces.views import LoginRequiredMixin

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

    def get_queryset(self):
        qs = super(ArticlePostByColumnView, self).get_queryset()
        return qs.filter(column=self.kwargs['column_id'])


# 标签文章
class ArticlePostByTagView(ArticleMixin, ListView):

    def get_queryset(self):
        qs = super(ArticlePostByTagView, self).get_queryset()
        return qs.filter(tags__name__in=[self.kwargs['tag_name']])


# 文章内容
def article_detail(request, article_id):
    article = ArticlesPost.objects.get(id=article_id)
    article.total_views = article.total_views
    article.increase_views()
    # 评论
    comment_form = CommentForm()
    context = {'article': article,
               'comment_form': comment_form,
               # 生成树形评论
               'comments': Comment.objects.all(),
               }
    return render(request, 'article/article_detail.html', context=context)


# 发表文章
class ArticleCreateView(LoginRequiredMixin, ArticleMixin, CreateView):
    fields = ['title', 'column', 'tags', 'body']
    template_name = 'article/article_create.html'

    # def get_queryset(self):
    #     qs = super(ArticleCreateView, self).get_queryset()
    #     return qs.filter(user=self.request.user)

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