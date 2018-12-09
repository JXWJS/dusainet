from django.urls import path
from django.views.generic import TemplateView

app_name = 'aboutme'
urlpatterns = [
    # 自我简介
    path('footpoint/', TemplateView.as_view(template_name='aboutme/footpoint.html'), name='footpoint'),
]

