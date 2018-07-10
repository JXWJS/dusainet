from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from .models import Comment, AlbumComment
from .forms import CommentForm, AlbumCommentForm

from article.models import ArticlesPost
from album.models import Album


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


def album_comment(request, photo_id, reply_to=None):
    photo = get_object_or_404(Album, id=photo_id)
    comment = AlbumComment.objects.get(id=reply_to)

    if request.method == 'POST':
        comment_form = AlbumCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.photo = photo
            new_comment.user = request.user
            if reply_to == None:
                new_comment.reply_to = None
            else:
                new_comment.reply_to = comment.user
            new_comment.save()
            return redirect(reverse('album:album_list'))
        else:
            return HttpResponse('1')
    else:
        comment_form = AlbumCommentForm()
        if reply_to:
            return render(request, 'comments/album_comments_reply.html',
                          {'comment_form': comment_form,
                           'image': photo,
                           'reply_to': reply_to,
                           })
        return HttpResponse('2')
