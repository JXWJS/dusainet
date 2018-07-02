from django.shortcuts import render, get_object_or_404, redirect

# from .models import Comment
from .forms import CommentForm

from article.models import ArticlesPost


# Create your views here.


def post_comment(request, article_id):
    article = get_object_or_404(ArticlesPost, id=article_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(article)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = article.comments.all()
            context = {'post': article,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'article/article_detail.html', context=context)
    # # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(article)
