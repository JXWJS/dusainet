from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from comments.models import Comment, ReadBookComment

admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(ReadBookComment, MPTTModelAdmin)
