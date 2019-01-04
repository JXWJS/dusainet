from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'album'
urlpatterns = [
    # 列表
    path('', views.AlbumListView.as_view(), name='album_list'),
    # 暂未使用的管理页面
    path('manage/', views.album_manage, name='album_manage'),
    path('upload/', views.AlbumUpload.as_view(), name='album_upload'),
    url(r'^delete/(?P<image_id>\d+)/$', views.album_delete, name='album_delete'),
]

