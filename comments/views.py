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

from utils.utils import send_email_to_user


# Create your views here.

@login_required(login_url='/accounts/weibo/login/?process=login')
def post_comment(request, article_id, node_id=False):
    """
    博文回复视图
    :param article_id: 文章id
    :param node_id: 父级评论id
    """
    article = get_object_or_404(ArticlesPost, id=article_id)

    # 如果node_id存在，则获取父级评论对象
    if node_id:
        comment = Comment.objects.get(id=node_id)

    # 处理POST请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        # 创建新评论
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 对二级评论，赋值root节点的id
            if node_id:
                new_comment.parent_id = comment.get_root().id
                new_comment.reply_to = comment.user
                new_comment.save()

                # 对不是superuser的二级评论发送通知
                if not comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=comment.user,
                        verb='回复了你',
                        target=article,
                        description='article',
                        action_object=new_comment,
                    )
                    # 给绑定了邮箱的用户发送回复通知邮件；需扩展User模型增加开关通知字段
                    # if comment.user.email:
                    #     send_email_to_user(recipient=comment.user.email)
            else:
                new_comment.reply_to = None
                new_comment.save()

            # 给superuser发送通知
            notify.send(
                request.user,
                recipient=User.objects.filter(is_staff=1),
                verb='回复了你',
                target=article,
                description='article',
                action_object=new_comment,
            )

            # 给博主发送通知邮件
            send_email_to_user(recipient='dusaiphoto@foxmail.com')
            return redirect(article)

        else:
            comment_list = article.comments.all()
            context = {'post': article,
                       'form': comment_form,
                       'comment_list': comment_list,
                       }
            return render(request, 'article/article_detail.html', context=context)

    # 处理GET请求
    else:
        comment_form = CommentForm()
        return render(request, 'comments/reply_post_comment.html',
                      {'comment_form': comment_form,
                       'article_id': article_id,
                       'node_id': node_id,
                       'comment': comment,
                       })


@login_required(login_url='/accounts/weibo/login/?process=login')
def read_book_post_comment(request, article_id, node_id=False):
    """
    读书评论
    结构与文章评论类似
    暂未抽象到一起
    """
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
                    notify.send(
                        request.user,
                        recipient=comment.user,
                        verb='回复了你',
                        target=article,
                        description='readbook',
                        action_object=new_comment,
                    )
            else:
                new_comment.reply_to = None
                new_comment.save()

            # 发送通知
            notify.send(
                request.user,
                recipient=User.objects.filter(is_staff=1),
                verb='回复了你',
                target=article,
                description='readbook',
                action_object=new_comment,
            )
            send_email_to_user(recipient='dusaiphoto@foxmail.com')  # 给博主发送通知邮件
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


@login_required(login_url='/accounts/weibo/login/?process=login')
def album_comment(request, photo_id, reply_to=None):
    """
    相册的评论
    已废弃此功能
    """
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
