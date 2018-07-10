from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.

class ArticlesColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlesPost(models.Model):
    author = models.ForeignKey(User, related_name='article', on_delete=models.CASCADE)
    column = models.ForeignKey(ArticlesColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='column')
    title = models.CharField(max_length=200)

    # taggit
    tags = TaggableManager(blank=True)

    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)

    avatar_thumbnail = ProcessedImageField(upload_to='image/article/avatar_thumbnail/',
                                           processors=[ResizeToFit(width=176)],
                                           format='JPEG',
                                           options={'quality': 100},
                                           blank=True,
                                           null=True)
    url = models.URLField(blank=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 统计浏览量
    def increase_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])

    # 统计评论数
    def increase_comments(self):
        self.total_comments += 1
        self.save(update_fields=['total_comments'])
