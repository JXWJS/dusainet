# Generated by Django 2.0.6 on 2018-07-23 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_articlespost_course_sequence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlespost',
            name='total_comments',
        ),
    ]
