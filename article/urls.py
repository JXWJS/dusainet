from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    # 文章列表
    url(r'^article-list/$', views.ArticlePostView.as_view(), name='article_list'),
    url(r'^article-list-by-column/(?P<column_id>\d+)/$',
        views.ArticlePostByColumnView.as_view(), name='article_list_by_column'),
    url(r'^article-list-by-tag/(?P<tag_name>\w+)/$',
        views.ArticlePostByTagView.as_view(), name='article_list_by_tag'),
    # 文章内容
    url(r'^article-detail/(?P<article_id>\d+)/$', views.article_detail, name='article_detail'),
    # 写文章
    url(r'^article-create/$', views.ArticleCreateView.as_view(), name='article_create'),
]