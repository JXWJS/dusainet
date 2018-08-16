from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class ReadBook(models.Model):
    author = models.ForeignKey(User, related_name='read_book_article', on_delete=models.CASCADE)

    writer = models.CharField(max_length=100, blank=True, null=True)
    book_page = models.PositiveIntegerField(blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # 总分数
    total_score = models.FloatField(blank=True)
    # 实用度
    practicality = models.PositiveIntegerField()
    # 趣味性
    interesting = models.PositiveIntegerField()
    # 易读性
    readability = models.PositiveIntegerField()
    # 专业度
    professionalism = models.PositiveIntegerField()
    # 装订质量
    binding_quality = models.PositiveIntegerField()


    total_views = models.PositiveIntegerField(default=0)
    # 缩略图
    avatar_thumbnail = ProcessedImageField(upload_to='image/read_book/avatar_thumbnail/',
                                           processors=[ResizeToFill(150, 200)],
                                           format='JPEG',
                                           options={'quality': 100},
                                           blank=True,
                                           null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('readbook:book_detail', args=[self.id])

    # 统计浏览量
    def increase_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_score = round((0.3*self.practicality + 0.3*self.interesting + 0.2*self.readability
                      + 0.1*self.professionalism + 0.1*self.binding_quality), 1)
        super(ReadBook, self).save()