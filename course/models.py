from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.

class Course(models.Model):
    """
    教程模型
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    created = models.DateField(default=timezone.now)
    is_finished = models.BooleanField(default=False, verbose_name='已完结')

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
