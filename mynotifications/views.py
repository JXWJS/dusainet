from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from article.models import ArticlesPost
from readbook.models import ReadBook
from vlog.models import Vlog


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification(request):
    """
    通知界面
    """
    unread_notify = request.user.notifications.unread()
    return render(
        request,
        'notifications/my_notification.html',
        {'unread_notify': unread_notify},
    )


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_all_as_read(request):
    """
    标记所有信息为已读
    """
    request.user.notifications.mark_all_as_read()
    return redirect('my_notifications:notify_box')


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_as_read(request,
                                       article_id,
                                       notify_id,
                                       article_type):
    """
    标记点击过的信息为已读
    """
    if article_type == 'article':
        article = ArticlesPost.objects.get(id=article_id)

    elif article_type == 'readbook':
        article = ReadBook.objects.get(id=article_id)

    else:
        article = Vlog.objects.get(id=article_id)

    request.user.notifications.get(id=notify_id).mark_as_read()
    return redirect(article)
