# Generated by Django 2.0.6 on 2019-01-25 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0031_auto_20190121_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_reply_to', to=settings.AUTH_USER_MODEL, verbose_name='评论给'),
        ),
    ]
