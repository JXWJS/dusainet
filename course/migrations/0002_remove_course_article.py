# Generated by Django 2.0.6 on 2018-07-10 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='article',
        ),
    ]
