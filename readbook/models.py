from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class ReadBook(models.Model):
    author = models.ForeignKey(
        User,
        related_name='read_book_article',
        on_delete=models.CASCADE,
        verbose_name='发布人',
    )

    comments = GenericRelation(Comment)

    writer = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='作者',
    )

    book_page = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='页数',
    )

    price = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='价格',
    )

    title = models.CharField(max_length=200, verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # 总分数
    total_score = models.FloatField(blank=True, verbose_name='总分数')
    # 实用度
    practicality = models.PositiveIntegerField(verbose_name='实用度')
    # 趣味性
    interesting = models.PositiveIntegerField(verbose_name='趣味性')
    # 易读性
    readability = models.PositiveIntegerField(verbose_name='易读性')
    # 专业度
    professionalism = models.PositiveIntegerField(verbose_name='专业度')
    # 装订质量
    binding_quality = models.PositiveIntegerField(verbose_name='装订')

    total_views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    # 缩略图
    avatar_thumbnail = ProcessedImageField(
        upload_to='image/read_book/%Y%m%d',
        processors=[ResizeToFill(150, 200)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        verbose_name='缩略图',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = '读书'

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('readbook:book_detail', args=[self.id])

    # 统计浏览量
    def increase_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.total_score = round(
            (0.3 * self.practicality
             + 0.3 * self.interesting
             + 0.2 * self.readability
             + 0.1 * self.professionalism
             + 0.1 * self.binding_quality), 1)
        super(ReadBook, self).save()
