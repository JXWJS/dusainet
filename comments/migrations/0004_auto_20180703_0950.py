# Generated by Django 2.0.6 on 2018-07-03 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20180702_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_time',)},
        ),
    ]