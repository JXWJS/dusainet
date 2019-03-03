from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment


class BookColumn(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name='标题')

    class Meta:
        verbose_name_plural = '栏目'

    def __str__(self):
        return self.title


class BookTag(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name='标题')

    class Meta:
        verbose_name_plural = '标签'

    def __str__(self):
        return self.title


class BookType(models.Model):
    """
    article栏目
    """
    title = models.CharField(max_length=100, blank=True, verbose_name='标题')

    class Meta:
        verbose_name_plural = '类型'

    def __str__(self):
        return self.title


# Create your models here.
class ReadBook(models.Model):
    author = models.ForeignKey(
        User,
        related_name='read_book_article',
        on_delete=models.CASCADE,
        verbose_name='发布人',
    )

    column = models.ForeignKey(BookColumn, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.ForeignKey(BookTag, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.ForeignKey(BookType, on_delete=models.SET_NULL, blank=True, null=True)

    title = models.CharField(max_length=200, verbose_name='标题')
    url = models.URLField(blank=True)

    comments = GenericRelation(Comment)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('column', 'tag', 'type')
        verbose_name_plural = '知识'

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('readbook:book_detail', args=[self.id])
