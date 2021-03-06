# Generated by Django 3.2.2 on 2021-05-21 09:42

import cinema_site.services.media_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0003_auto_20210520_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=cinema_site.services.media_services.UploadToPathAndRename('images')),
        ),
    ]
