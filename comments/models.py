from django.db import models
from django.contrib.auth.models import User

from article.models import ArticlesPost

from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    article = models.ForeignKey(ArticlesPost, on_delete=models.CASCADE, related_name='comments')
    user = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # mptt
    # name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]
