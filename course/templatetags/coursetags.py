from django.template import Library
from course.models import Course

register = Library()

@register.simple_tag
def course_total_views(course_id):
    articles = Course.objects.get(id=course_id).article.all()
    views = 0
    for article in articles:
        views += article.total_views
    return views

@register.simple_tag
def course_total_articles(course_id):
    total_articles = Course.objects.get(id=course_id).article.count()
    return total_articles