from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
import os
from random import randint

from imagekit.models import ProcessedImageField


# 生成放置 avartar 的文件夹
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # 这里的id是User表的id
    return os.path.join('user', str(instance.user_id), "avatar", filename)


class UserInfo(models.Model):
    # User.id OntToOneField
    user_id = models.PositiveIntegerField()

    # avatar
    avatar = ProcessedImageField(
        upload_to=user_directory_path,
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        verbose_name='头像',
    )

    def __str__(self):
        user = User.objects.get(id=self.user_id)
        return user.username


def get_default_avatar_url():
    return '/static/img/user_default_avatar/0' + str(randint(1, 9)) + '.svg'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_avatar_url = get_default_avatar_url()
        UserInfo.objects.create(user_id=instance.id, avatar=default_avatar_url)