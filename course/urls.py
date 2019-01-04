from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'course'
urlpatterns = [
    path(
        '',
        views.CourseListView.as_view(),
        name='course_list',
    ),
    url(
        r'^articles-list/(?P<course_id>\d+)/$',
        views.course_articles_list,
        name='course_articles_list',
    ),
]

