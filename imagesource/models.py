from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.
class ImageSource(models.Model):
    created = models.DateField(default=timezone.now)
    avatar_thumbnail = ProcessedImageField(upload_to='image/image_source/avatar_thumbnail/',
                                           processors=[ResizeToFit(width=2400, upscale=False)],
                                           format='JPEG',
                                           options={'quality': 100},)