# Generated by Django 3.2.2 on 2021-05-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0029_rename_created_news_publication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='publication',
        ),
        migrations.AddField(
            model_name='news',
            name='sdgdg',
            field=models.DateField(default='2020-09-15'),
            preserve_default=False,
        ),
    ]
