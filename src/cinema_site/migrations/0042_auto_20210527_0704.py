# Generated by Django 3.2.2 on 2021-05-27 07:04

import cinema_site.services.media_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0041_auto_20210527_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='coordinates',
            field=models.TextField(max_length=800),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='logo',
            field=models.ImageField(upload_to=cinema_site.services.media_services.UploadToPathAndRename('contacts/logos')),
        ),
    ]
