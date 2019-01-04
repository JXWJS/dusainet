from django.db import models
from django.contrib.auth.models import User

from article.models import ArticlesPost
from readbook.models import ReadBook
from vlog.models import Vlog

from mptt.models import MPTTModel, TreeForeignKey


# 博文的评论
class Comment(MPTTModel):
    """
    博文评论
    与读书、视频的评论model只有外键的差别
    generic foreignkey?
    """
    article = models.ForeignKey(
        ArticlesPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='文章',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_user',
        verbose_name='评论者',
    )

    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(auto_now_add=True)

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
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

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]


# 读书版块的评论
class ReadBookComment(MPTTModel):
    article = models.ForeignKey(
        ReadBook,
        on_delete=models.CASCADE,
        related_name='readbook_comments',
        verbose_name='文章',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='readbook_comments_user',
        verbose_name='评论者',
    )
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(auto_now_add=True)

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='readbook_comments_reply_to',
        verbose_name='评论给',
    )

    # mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父级',
    )

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]


class VlogComment(MPTTModel):
    """
    vlog评论
    """
    article = models.ForeignKey(
        Vlog,
        on_delete=models.CASCADE,
        related_name='vlog_comments',
        verbose_name='文章',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vlog_comments_user',
        verbose_name='评论者',
    )

    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(auto_now_add=True)

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='vlog_comments_reply_to',
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

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]
