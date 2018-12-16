from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    # 文章的回复
    path(
        'post-comment/<int:article_id>/',
        views.CommentCreateView.as_view(),
        name='post_comment'
    ),
    path(
        'reply-post-comment/<int:article_id>/<int:node_id>/<article_type>/',
        views.CommentCreateView.as_view(),
        name='reply_post_comment'
    ),

    # 读书版块的回复
    url(
        r'^read-book-post-comment/(?P<article_id>\d+)/$',
        views.CommentCreateView.as_view(),
        name='read_book_post_comment'
    ),
    path(
        'read-book-reply-post-comment/<int:article_id>/<int:node_id>/<article_type>/',
        views.CommentCreateView.as_view(),
        name='read_book_reply_post_comment'
    ),

    # vlog的回复
    path(
        'vlog-post-comment/<int:article_id>/',
        views.CommentCreateView.as_view(),
        name='vlog_post_comment'
    ),
    path(
        'vlog-reply-post-comment/<int:article_id>/<int:node_id>/<article_type>/',
        views.CommentCreateView.as_view(),
        name='vlog_reply_post_comment'
    ),
]
