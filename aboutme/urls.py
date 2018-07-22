from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'aboutme'
urlpatterns = [
    path('', TemplateView.as_view(template_name='aboutme/aboutme.html'), name='me'),
    path('footpoint/', TemplateView.as_view(template_name='aboutme/footpoint.html'), name='footpoint'),
]

