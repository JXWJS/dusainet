from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    # 文章回复
    url(r'^post-comment/(?P<article_id>\d+)/$', views.post_comment, name='post_comment'),
    url(r'^reply-post-comment/(?P<article_id>\d+)/(?P<node_id>\d+)/',
        views.post_comment, name='reply_post_comment'),
    # 读书回复
    url(r'^read-book-post-comment/(?P<article_id>\d+)/$', views.read_book_post_comment, name='read_book_post_comment'),
    url(r'^read-book-reply-post-comment/(?P<article_id>\d+)/(?P<node_id>\d+)/',
        views.read_book_post_comment, name='read_book_reply_post_comment'),
    # 图片回复
    url(r'^album-comment/(?P<photo_id>\d+)/$', views.album_comment, name='album_comment'),
    url(r'^album-comment/(?P<photo_id>\d+)/(?P<reply_to>\d+)/$', views.album_comment, name='reply_album_comment'),
]
