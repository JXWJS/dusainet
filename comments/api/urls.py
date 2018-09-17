from django.urls import path

from comments.api.views import (
CommentListAPIView,
CommentDetailAPIView,
CommentCreateAPIView,
)

app_name = 'comment'

urlpatterns = [
    path('create/', CommentCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='detail'),
    path('list/', CommentListAPIView.as_view(), name='list'),
]
