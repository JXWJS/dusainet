# Generated by Django 2.0.6 on 2018-07-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_course_article'),
        ('article', '0008_auto_20180710_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlespost',
            name='course',
            field=models.ManyToManyField(related_name='article', to='course.Course'),
        ),
    ]