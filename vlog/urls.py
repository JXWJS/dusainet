from django.urls import path
from . import views

app_name = 'vlog'

urlpatterns = [
    path('list/', views.VlogListView.as_view(), name='list'),
    path('detail/<int:pk>', views.VlogDetailView.as_view(), name='detail'),
]