from django.shortcuts import render
from django.views.generic import ListView

from .models import Course


# Create your views here.
class CourseListView(ListView):
    template_name = 'course/course_list.html'
    context_object_name = 'courses'
    model = Course


class CourseArticlesListView(ListView):
    template_name = 'course/course_articles_list.html'
    context_object_name = 'course_articles'
    model = Course

    def get_queryset(self):
        qs = super(CourseArticlesListView, self).get_queryset()
        return qs.get(id=self.kwargs['course_id']).article.all().order_by('course_sequence')
