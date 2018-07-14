from django.contrib import admin
from .models import ArticlesPost, ArticlesColumn

# Register your models here.
class ArticlesPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id', 'course_sequence', 'total_views', 'total_comments')
    list_filter = ('course_id', 'column_id')

admin.site.register(ArticlesPost, ArticlesPostAdmin)
admin.site.register(ArticlesColumn)