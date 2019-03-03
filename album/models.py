from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from uuslug import slugify


# Create your models here.
class Album(models.Model):
    """
    照片墙
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='album',
        verbose_name='发布员',
    )

    url = models.URLField(blank=True)
    slug = models.SlugField(max_length=500, blank=True)
    # 需要展示的内容
    title = models.CharField(max_length=300, verbose_name="标题")
    description = models.TextField(blank=True, verbose_name='简介')
    image = models.ImageField(upload_to='image/album/%Y%m%d', blank=True, null=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    # 点赞功能。暂未使用
    total_likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = '照片墙'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    # 评论数+1
    def increase_comments(self):
        self.total_likes += 1
        self.save(update_fields=['total_likes'])

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('album:album_list')
