from django.db import models
from django.contrib.auth.models import User

from article.models import ArticlesPost

from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    article = models.ForeignKey(ArticlesPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comments_reply_to')

    # mptt树形结构
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['-created_time']

    def __str__(self):
        return self.body[:20]
