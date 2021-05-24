# Generated by Django 3.2.2 on 2021-05-24 06:54

import cinema_site.services.media_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0010_auto_20210524_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='banner',
            field=models.ImageField(upload_to=cinema_site.services.media_services.UploadToPathAndRename('images/cinemas/<django.db.models.fields.CharField>/banners')),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='logo',
            field=models.ImageField(upload_to=cinema_site.services.media_services.UploadToPathAndRename('images/cinemas/<django.db.models.fields.CharField>/logos')),
        ),
    ]
