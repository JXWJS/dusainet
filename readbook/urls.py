from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'readbook'
urlpatterns = [
    url(
        r'^book-list/$',
        views.ReadBookListView.as_view(),
        name='book_list',
    ),

    url(
        r'^book-detail/(?P<article_id>\d+)/$',
        views.read_book_detail,
        name='book_detail',
    ),
]

