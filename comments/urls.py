from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    # 一级回复
    path(
        'post-comment/<int:article_id>/',
        views.CommentCreateView.as_view(),
        name='post_comment'
    ),

    # 二级回复
    path(
        'reply-post-comment/<int:article_id>/<int:node_id>/<article_type>/',
        views.CommentCreateView.as_view(),
        name='reply_post_comment'
    ),
]
