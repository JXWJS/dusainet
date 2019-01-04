from django.urls import path

from . import views

app_name = 'imagesource'
urlpatterns = [
    path(
        '',
        views.ImageSourceListView.as_view(),
        name='imagesource_list',
    ),
]

