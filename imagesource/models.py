from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.
class ImageSource(models.Model):
    created = models.DateTimeField(default=timezone.now)
    avatar_thumbnail = ProcessedImageField(
        upload_to='image/image_source/%Y%m%d',
        processors=[ResizeToFit(width=1200, upscale=False)],
        format='JPEG',
        options={'quality': 100},
        verbose_name='图片',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = '图库'

    def __str__(self):
        return str(self.created)
