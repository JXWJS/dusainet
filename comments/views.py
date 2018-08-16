from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from notifications.signals import notify

from .models import Comment, AlbumComment, ReadBookComment
from .forms import CommentForm, AlbumCommentForm, ReadBookCommentForm

from article.models import ArticlesPost
from album.models import Album
from readbook.models import ReadBook


# Create your views here.

# 文章评论
@login_required(login_url='/accounts/weibo/login/?process=login')
def post_comment(request, article_id, node_id=False):
    article = get_object_or_404(ArticlesPost, id=article_id)
    # 判断二级评论
    if node_id:
        comment = Comment.objects.get(id=node_id)
    # 处理POST请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            if node_id:
                # 对二级评论，赋值root节点的id
                new_comment.parent_id = comment.get_root().id
                new_comment.reply_to = comment.user
                new_comment.save()
                # 对不是superuser的二级评论发送通知
                if not comment.user.is_superuser:
                    notify.send(request.user, recipient=comment.user, verb='回复了你', target=article,
                                description='article', action_object=new_comment)
            else:
                new_comment.reply_to = None
                new_comment.save()
            # 给superuser发送通知
            notify.send(request.user, recipient=User.objects.filter(is_staff=1), verb='回复了你', target=article,
                        description='article', action_object=new_comment)
            return redirect(article)

        else:
            comment_list = article.comments.all()
            context = {'post': article,
                       'form': comment_form,
                       'comment_list': comment_list
                       }
            return render(request, 'article/article_detail.html', context=context)
    # 处理GET二级评论请求
    else:
        comment_form = CommentForm()
        return render(request, 'comments/reply_post_comment.html',
                      {'comment_form': comment_form,
                       'article_id': article_id,
                       'node_id': node_id,
                       'comment': comment
                       })


# 读书评论，结构与文章评论类似，未做抽象
@login_required(login_url='/accounts/weibo/login/?process=login')
def read_book_post_comment(request, article_id, node_id=False):
    article = get_object_or_404(ReadBook, id=article_id)
    if node_id:
        comment = ReadBookComment.objects.get(id=node_id)
    if request.method == 'POST':
        comment_form = ReadBookCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            if node_id:
                new_comment.parent_id = comment.get_root().id
                new_comment.reply_to = comment.user
                new_comment.save()
                # 对不是superuser的二级评论发送通知
                if not comment.user.is_superuser:
                    notify.send(request.user, recipient=comment.user, verb='回复了你', target=article,
                                description='readbook', action_object=new_comment)
            else:
                new_comment.reply_to = None
                new_comment.save()

            # 发送通知
            notify.send(request.user, recipient=User.objects.filter(is_staff=1), verb='回复了你', target=article,
                        description='readbook', action_object=new_comment)

            return redirect(article)
        else:
            comment_list = article.readbook_comments.all()
            context = {'post': article,
                       'form': comment_form,
                       'comment_list': comment_list
                       }
            return render(request, 'readbook/book_detail.html', context=context)
    else:
        comment_form = ReadBookCommentForm()
        return render(request, 'comments/read_book_reply_post_comment.html',
                      {'comment_form': comment_form,
                       'article_id': article_id,
                       'node_id': node_id,
                       'comment': comment
                       })


# 相册评论
@login_required(login_url='/accounts/weibo/login/?process=login')
def album_comment(request, photo_id, reply_to=None):
    photo = get_object_or_404(Album, id=photo_id)

    if request.method == 'POST':
        comment_form = AlbumCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.photo = photo
            new_comment.user = request.user
            if reply_to == None:
                new_comment.reply_to = None
            else:
                comment = AlbumComment.objects.get(id=reply_to)
                new_comment.reply_to = comment.user
                # 对不是superuser的二级评论发送通知
                if not comment.user.is_superuser:
                    notify.send(request.user, recipient=comment.user, verb='回复了你', target=photo,
                                description='album', action_object=new_comment)
            new_comment.save()

            # 发送通知
            notify.send(request.user, recipient=User.objects.filter(is_staff=1), verb='回复了你', target=photo,
                        description='album', action_object=new_comment)

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
