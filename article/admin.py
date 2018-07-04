from django.contrib import admin
from .models import ArticlesPost, ArticlesColumn

# Register your models here.
admin.site.register(ArticlesPost)
admin.site.register(ArticlesColumn)