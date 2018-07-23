from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'my_notifications'
urlpatterns = [
    path('notify-box/', views.comments_notification, name='notify_box'),
    path('notify-box/mark-all-read', views.comments_notification_mark_all_as_read, name='mark_all_read'),
    path('notify-box/mark-as-read/<int:article_id>/<int:notify_id>/<int:is_readbook>/<int:is_album>/',
         views.comments_notification_mark_as_read, name='mark_as_read'),
]