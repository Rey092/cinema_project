# Generated by Django 3.2.2 on 2021-05-29 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0043_auto_20210529_0453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='text',
        ),
        migrations.RemoveField(
            model_name='image',
            name='url',
        ),
    ]
