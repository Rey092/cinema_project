# Generated by Django 3.2.2 on 2021-05-26 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0033_rename_video_url_news_trailer_url'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='News',
            new_name='Article',
        ),
    ]