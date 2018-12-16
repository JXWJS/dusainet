from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from comments.models import Comment, ReadBookComment, VlogComment

admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(ReadBookComment, MPTTModelAdmin)
admin.site.register(VlogComment, MPTTModelAdmin)
