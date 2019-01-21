from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor.fields import RichTextField


# 博文的评论
class Comment(MPTTModel):
    """
    评论
    GenericForeignkey
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_user',
        verbose_name='评论者',
    )

    body = RichTextField(verbose_name='正文')
    created_time = models.DateTimeField(auto_now_add=True)

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments_reply_to',
        verbose_name='评论给'
    )

    # mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name='父级',
    )

    # 软删除标记
    is_deleted = models.BooleanField(default=False)
    is_deleted_by_staff = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]
