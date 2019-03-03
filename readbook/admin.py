from django.contrib import admin
from .models import ReadBook, BookType, BookTag, BookColumn

# Register your models here.
admin.site.register(ReadBook)
admin.site.register(BookType)
admin.site.register(BookTag)
admin.site.register(BookColumn)