from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Vlog(models.Model):
    """
    vlog model
    """
    author = models.ForeignKey(
        User,
        related_name='vlog',
        on_delete=models.CASCADE,
        verbose_name='作者',
    )

    title = models.CharField(max_length=200, verbose_name='标题')
    # 简介正文
    body = models.TextField(
        blank=True,
        verbose_name='正文',
    )
    # 缩略图 url
    avatar_url = models.URLField(blank=True, verbose_name='标题图链接')
    # video url
    video_url = models.URLField(verbose_name='视频链接')

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = '视频'

    def __str__(self):
        return self.title

    # 获取vlog detail地址
    def get_absolute_url(self):
        return reverse('vlog:detail', args=[self.id])

    # 统计浏览量
    def increase_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])
