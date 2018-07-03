from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import ArticlesPost
from comments.models import Comment
from comments.forms import CommentForm


# Create your views here.

# 文章列表
class ArticlePostView(ListView):
    model = ArticlesPost
    template_name = 'article/article_list.html'
    context_object_name = 'articles'


def article_detail(request, article_id):
    article = ArticlesPost.objects.get(id=article_id)
    article.total_views = article.total_views
    article.increase_views()
    # 评论
    comment_form = CommentForm()
    context = {'article': article,
               'comment_form': comment_form,
               # 生成树形评论
               'comments': Comment.objects.all()
               }
    return render(request, 'article/article_detail.html', context=context)
