# Generated by Django 3.2.2 on 2021-06-11 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0051_rename_reverse_logger_referer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logger',
            name='referer',
            field=models.URLField(max_length=300, null=True),
        ),
    ]