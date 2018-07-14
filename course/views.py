from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse


from .models import Course


# Create your views here.
class CourseListView(ListView):
    template_name = 'course/course_list.html'
    context_object_name = 'courses'
    model = Course


# class CourseArticlesListView(ListView):
#     template_name = 'course/course_articles_list.html'
#     context_object_name = 'course_articles'
#     model = Course
#
#     def get_queryset(self):
#         qs = super(CourseArticlesListView, self).get_queryset()
#         return qs.get(id=self.kwargs['course_id']).article.all().order_by('course_sequence')

def course_articles_list(request, course_id):
    try:
        article = Course.objects.get(id=course_id).article.order_by('course_sequence')[0]
        return redirect(article)
    except:
        return HttpResponse('还没有文章')