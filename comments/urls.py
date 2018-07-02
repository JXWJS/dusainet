from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^post/(?P<comment_id>\d+)/$', views.post_comment, name='post_comment'),
]
