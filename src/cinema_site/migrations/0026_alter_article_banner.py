# Generated by Django 3.2.2 on 2021-05-25 11:47

import cinema_site.services.media_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0025_auto_20210525_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='banner',
            field=models.ImageField(default=1, upload_to=cinema_site.services.media_services.UploadToPathAndRename('articles/banners')),
            preserve_default=False,
        ),
    ]
