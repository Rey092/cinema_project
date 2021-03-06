# Generated by Django 3.2.2 on 2021-06-06 13:23

import cinema_site.services.media_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0048_remove_contacts_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='banner',
            field=models.ImageField(default=1, upload_to=cinema_site.services.media_services.UploadToPathAndRename('contacts/banner')),
            preserve_default=False,
        ),
    ]
