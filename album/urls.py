from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'album'
urlpatterns = [
    # 列表
    path('album-list/', views.AlbumListView.as_view(), name='album_list'),
    # 暂未使用的管理页面
    path('album-manage/', views.album_manage, name='album_manage'),
    path('album-upload/', views.AlbumUpload.as_view(), name='album_upload'),
    url(r'^album-delete/(?P<image_id>\d+)/$', views.album_delete, name='album_delete'),
]

