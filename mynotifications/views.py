from django.shortcuts import render
from notifications.models import Notification


# Create your views here.

def comments_notification(request):
    unread_notify = request.user.notifications.unread()
    return render(request, 'notifications/my_notification.html', {'unread_notify': unread_notify})


def comments_notification_mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    unread_notify = request.user.notifications.unread()
    return render(request, 'notifications/my_notification.html', {'unread_notify': unread_notify})
