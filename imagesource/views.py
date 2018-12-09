from django.shortcuts import render
from django.views.generic import ListView
from utils.utils import PaginatorMixin

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from .models import ImageSource


# Create your views here.
class ImageSourceListView(PaginatorMixin,
                          LoginRequiredMixin,
                          StaffuserRequiredMixin,
                          ListView):
    """
    图库list
    """
    model = ImageSource
    template_name = 'imagesource/image_source_list.html'
    context_object_name = 'images'
