from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    # 文章列表
    url(r'^article-list/$', views.ArticlePostView.as_view(), name='article_list'),
    # 最热文章
    url(r'^article-list-by-most-viewed/$', views.ArticlePostByMostViewedView.as_view(),
        name='article_list_by_most_viewed'),
    url(r'^article-list-by-most-viewed/(?P<column_id>\d+)/$', views.ArticlePostByMostViewedView.as_view(),
        name='article_list_by_column_most_viewed'),
    # 栏目文章
    url(r'^article-list-by-column/(?P<column_id>\d+)/$',
        views.ArticlePostByColumnView.as_view(), name='article_list_by_column'),
    # 标签文章
    url(r'^article-list-by-tag/(?P<tag_name>\w+)/$',
        views.ArticlePostByTagView.as_view(), name='article_list_by_tag'),
    # 文章内容
    url(r'^article-detail/(?P<article_id>\d+)/$', views.article_detail, name='article_detail'),
    # 写文章
    url(r'^article-create/$', views.ArticleCreateView.as_view(), name='article_create'),
    # 更新文章
    url(r'article-update/(?P<pk>\d+)/$', views.ArticleUpdateView.as_view(), name='article_update'),

]
