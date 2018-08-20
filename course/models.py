from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateField(default=timezone.now)
    is_finished = models.BooleanField(default=False)

    avatar_thumbnail = ProcessedImageField(upload_to='image/course/%Y%m%d',
                                           processors=[ResizeToFill(256, 144)],
                                           format='JPEG',
                                           options={'quality': 100},
                                           blank=True,
                                           null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)