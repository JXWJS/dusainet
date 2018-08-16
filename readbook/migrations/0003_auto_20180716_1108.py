# Generated by Django 2.0.6 on 2018-07-16 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('readbook', '0002_auto_20180715_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='readbook',
            name='writer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='readbook',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='read_book_article', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
