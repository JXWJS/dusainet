from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from article.models import ArticlesPost
from album.models import Album
from readbook.models import ReadBook
from vlog.models import Vlog


# Create your views here.
# 通知界面
@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification(request):
    unread_notify = request.user.notifications.unread()
    return render(
        request,
        'notifications/my_notification.html',
        {'unread_notify': unread_notify},
    )


# 标记全部已读
@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    unread_notify = request.user.notifications.unread()
    return render(
        request,
        'notifications/my_notification.html',
        {'unread_notify': unread_notify},
    )


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_as_read(request,
                                       article_id,
                                       notify_id,
                                       article_type):
    if article_type == 'article':
        article = ArticlesPost.objects.get(id=article_id)

    elif article_type == 'readbook':
        article = ReadBook.objects.get(id=article_id)

    else:
        article = Vlog.objects.get(id=article_id)

    request.user.notifications.get(id=notify_id).mark_as_read()
    return redirect(article)
