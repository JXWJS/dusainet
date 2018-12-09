from django.shortcuts import redirect
from django.views.generic import ListView
from django.http import HttpResponse

from .models import Course


# Create your views here.
class CourseListView(ListView):
    """
    教程list
    """
    template_name = 'course/course_list.html'
    context_object_name = 'courses'
    model = Course


def course_articles_list(request, course_id):
    """
    教程中course_sequence最小的博文
    """
    try:
        article = Course.objects.get(id=course_id).article.order_by('course_sequence')[0]
        return redirect(article)
    except:
        return HttpResponse('还没有文章')
