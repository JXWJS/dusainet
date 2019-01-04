from django.shortcuts import render
from django.views.generic import ListView

from .models import ReadBook

from comments.models import ReadBookComment
from comments.forms import ReadBookCommentForm

from utils.utils import PaginatorMixin


# Create your views here.

# 读书列表
class ReadBookListView(PaginatorMixin, ListView):
    model = ReadBook
    template_name = 'readbook/book_list.html'
    context_object_name = 'articles'


# 文章内容
def read_book_detail(request, article_id):
    article = ReadBook.objects.get(id=article_id)
    article.increase_views()

    # 传递给模板文章类型，用于评论表单区分
    article_type = 'readbook'

    # 评论
    comment_form = ReadBookCommentForm()
    context = {'article': article,
               'comment_form': comment_form,
               # 生成树形评论
               'comments': ReadBookComment.objects.filter(article_id=article_id),
               'article_type': article_type,
               }
    return render(request, 'readbook/book_detail.html', context=context)
