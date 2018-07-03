from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^post-comment/(?P<article_id>\d+)/$', views.post_comment, name='post_comment'),
    url(r'^reply-post-comment/(?P<article_id>\d+)/(?P<node_id>\d+)/',
        views.reply_post_comment, name='reply_post_comment'),
]
