from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class GithubRepo(models.Model):
    """
    Github仓库数据的小卡片
    """
    user = models.CharField(max_length=100, verbose_name='拥有者', default='stacklens')
    repo = models.CharField(max_length=500, verbose_name='仓库名')
    description = models.CharField(max_length=500, verbose_name='简介')

    class Meta:
        verbose_name_plural = 'Github仓库'

    def __str__(self):
        return self.repo


class Course(models.Model):
    """
    教程模型
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    created = models.DateField(default=timezone.now)
    is_finished = models.BooleanField(default=False, verbose_name='已完结')

    # 教程标题下面的Github小卡片
    github_repo = models.ForeignKey(
        GithubRepo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    avatar_thumbnail = ProcessedImageField(
        upload_to='image/course/%Y%m%d',
        processors=[ResizeToFill(256, 144)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        verbose_name='缩略图',
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)
        verbose_name_plural = '教程'
