from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'readbook'
urlpatterns = [
    url(r'^book-list/$', views.ReadBookListView.as_view(), name='book_list'),
    url(r'^book-detail/(?P<book_id>\d+)/$', views.ReadBookDetailView.as_view(), name='book_detail'),
]

