from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'imagesource'
urlpatterns = [
    path('imagesource-list/', views.ImageSourceListView.as_view(), name='imagesource_list'),
]

