from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required

from article.models import ArticlesPost
from album.models import Album
from readbook.models import ReadBook


# Create your views here.
# 通知界面
@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification(request):
    unread_notify = request.user.notifications.unread()
    return render(request, 'notifications/my_notification.html', {'unread_notify': unread_notify})


# 标记全部已读
@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    unread_notify = request.user.notifications.unread()
    return render(request, 'notifications/my_notification.html', {'unread_notify': unread_notify})


@login_required(login_url='/accounts/weibo/login/?process=login')
def comments_notification_mark_as_read(request, article_id, notify_id, is_readbook=False, is_album=False):
    if is_album:
        article = Album.objects.get(id=article_id)

    elif is_readbook:
        article = ReadBook.objects.get(id=article_id)

    else:
        article = ArticlesPost.objects.get(id=article_id)

    request.user.notifications.get(id=notify_id).mark_as_read()
    return redirect(article)
