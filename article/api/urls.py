from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    # 文章列表
    url(r'^list/$', views.ArticleListAPIView.as_view(), name='list'),
    # # 最热文章
    # url(r'^article-list-by-most-viewed/$', views.ArticlePostByMostViewedView.as_view(),
    #     name='article_list_by_most_viewed'),
    # url(r'^article-list-by-most-viewed/(?P<column_id>\d+)/$', views.ArticlePostByMostViewedView.as_view(),
    #     name='article_list_by_column_most_viewed'),
    # # 栏目文章
    # url(r'^article-list-by-column/(?P<column_id>\d+)/$',
    #     views.ArticlePostByColumnView.as_view(), name='article_list_by_column'),
    # # 标签文章
    # url(r'^article-list-by-tag/(?P<tag_name>\w+)/$',
    #     views.ArticlePostByTagView.as_view(), name='article_list_by_tag'),
    # 删改查
    url(r'^(?P<pk>\d+)/$', views.ArticleUpdateAPIView.as_view(), name='detail'),
    # 增
    url(r'^create/$', views.ArticleCreateAPIView.as_view(), name='create'),

]
