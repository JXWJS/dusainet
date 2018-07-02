from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    # views
    url(r'^article-list/$', views.ArticlePostView.as_view(), name='article_list'),
    url(r'^article-detail/(?P<article_id>\d+)/$', views.article_detail, name='article_detail'),
]