from django.shortcuts import render
from django.views.generic import ListView

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin, StaffuserRequiredMixin

from .models import ImageSource


# Create your views here.
class ImageSourceListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    model = ImageSource
    template_name = 'imagesource/image_source_list.html'
    context_object_name = 'images'
