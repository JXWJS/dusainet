from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'album'
urlpatterns = [
    path('album-list/', views.album_list, name='album_list'),
    path('album-manage/', views.album_manage, name='album_manage'),
    path('album-upload/', views.AlbumUpload.as_view(), name='album_upload'),
    url(r'^album-delete/(?P<image_id>\d+)/$', views.album_delete, name='album_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)