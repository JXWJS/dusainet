from django.shortcuts import render, get_object_or_404, redirect

from .models import Comment
from .forms import CommentForm

from article.models import ArticlesPost


# Create your views here.

# 评论文章
def post_comment(request, article_id):
    article = get_object_or_404(ArticlesPost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.reply_to = None
            new_comment.save()
            article.increase_comments()
            return redirect(article)
        else:
            comment_list = article.comments.all()
            context = {'post': article,
                       'form': comment_form,
                       'comment_list': comment_list
                       }
            return render(request, 'article/article_detail.html', context=context)
    else:
        comment_form = CommentForm()
        return redirect(article)


# 二级评论
def reply_post_comment(request, article_id, node_id):
    article = get_object_or_404(ArticlesPost, id=article_id)
    comment = Comment.objects.get(id=node_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            # 对二级评论，赋值root节点的id
            new_comment.parent_id = comment.get_root().id
            new_comment.reply_to = comment.user
            new_comment.save()
            article.increase_comments()
            return redirect(article)
    else:
        comment_form = CommentForm()
        return render(request, 'comments/reply_post_comment.html',
                      {'comment_form': comment_form,
                       'article_id': article_id,
                       'node_id': node_id,
                       'comment': comment
                       })
