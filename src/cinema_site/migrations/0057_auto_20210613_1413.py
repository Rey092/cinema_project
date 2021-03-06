# Generated by Django 3.2.2 on 2021-06-13 14:13

import cinema_site.services.media_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0056_backgroundimage_top_banners_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundimage',
            name='bg_format',
            field=models.CharField(choices=[('photo_bg', 'Фон-фото'), ('simple_bg', 'Простой фон')], default='simple_bg', max_length=10, verbose_name='Формат фона'),
        ),
        migrations.AlterField(
            model_name='backgroundimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cinema_site.services.media_services.UploadToPathAndRename('background')),
        ),
    ]
