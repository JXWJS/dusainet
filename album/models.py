from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from uuslug import slugify


# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album')
    url = models.URLField(blank=True)
    slug = models.SlugField(max_length=500, blank=True)
    # 需要展示的内容
    title = models.CharField(max_length=300)
    photographer = models.TextField(blank=True)
    location = models.TextField(blank=True)
    photo_time = models.TextField(blank=True)
    camera = models.TextField(blank=True)
    lens = models.TextField(blank=True)
    focal_length = models.TextField(blank=True)
    aperture = models.TextField(blank=True)
    exposure_time = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='image/album/%Y%m%d')
    created = models.DateField(auto_now_add=True, db_index=True)

    total_likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    # 统计喜欢
    def increase_comments(self):
        self.total_likes += 1
        self.save(update_fields=['total_likes'])

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('album:album_list')