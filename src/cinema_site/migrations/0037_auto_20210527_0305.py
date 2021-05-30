# Generated by Django 3.2.2 on 2021-05-27 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0036_alter_article_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='created',
            field=models.DateField(auto_now_add=True, default='2020-09-16'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]