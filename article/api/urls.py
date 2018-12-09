from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
    # 文章列表
    url(r'^list/$', views.ArticleListAPIView.as_view(), name='list'),
    # 删改查
    url(r'^(?P<pk>\d+)/$', views.ArticleUpdateAPIView.as_view(), name='detail'),
    # 增
    url(r'^create/$', views.ArticleCreateAPIView.as_view(), name='create'),

]
