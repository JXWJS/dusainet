from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    # 文章列表
    url(r'^article-list/$', views.ArticlePostView.as_view(), name='article_list'),

    # 文章内容
    url(
        r'^article-detail/(?P<article_id>\d+)/$',
        views.article_detail,
        name='article_detail',
    ),

    # 写新文章
    url(
        r'^article-create/$',
        views.ArticleCreateView.as_view(),
        name='article_create',
    ),

    # 更新文章
    url(
        r'article-update/(?P<pk>\d+)/$',
        views.ArticleUpdateView.as_view(),
        name='article_update',
    ),
]
