from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    # 发表一级回复
    path(
        'post-comment/<int:article_id>/',
        views.CommentCreateView.as_view(),
        name='post_comment'
    ),

    # 发表二级回复
    path(
        'reply-post-comment/<int:article_id>/<int:node_id>/<article_type>/',
        views.CommentCreateView.as_view(),
        name='reply_post_comment'
    ),

    # 软删除
    path(
        'soft-delete/',
        views.comment_soft_delete,
        name='soft_delete'
    ),
]
