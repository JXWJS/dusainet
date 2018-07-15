from django.shortcuts import render
from django.views.generic import ListView

from .models import ReadBook

# Create your views here.

class ReadBookListView(ListView):
    model = ReadBook
    template_name = 'readbook/book_list.html'
    context_object_name = 'books'

class ReadBookDetailView(ListView):
    model = ReadBook
    template_name = 'readbook/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        qs = super(ReadBookDetailView, self).get_queryset()
        return qs.get(id=self.kwargs['book_id'])