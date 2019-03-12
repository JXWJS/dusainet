from django.shortcuts import render
from django.views.generic import ListView

from .models import ReadBook

from comments.forms import CommentForm


# 读书列表
class ReadBookListView(ListView):
    model = ReadBook
    template_name = 'readbook/book_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        """
        获取上下文
        :return: context
        """
        context = super(ReadBookListView, self).get_context_data(**kwargs)

        # 更新信息
        code_articles = ReadBook.objects.filter(column__title='编程')
        unknown_articles = ReadBook.objects.filter(column__title='未归类')
        data = {'code_articles': code_articles,
                'unknown_articles': unknown_articles,
                }
        context.update(data)
        return context


# 文章内容
def read_book_detail(request, article_id):
    article = ReadBook.objects.get(id=article_id)

    # 传递给模板文章类型，用于评论表单区分
    article_type = 'readbook'

    # 评论
    comment_form = CommentForm()
    context = {'article': article,
               'comment_form': comment_form,
               # 生成树形评论
               'comments': article.comments.all(),
               'article_type': article_type,
               }
    return render(request, 'readbook/book_detail.html', context=context)
