# Generated by Django 3.2.2 on 2021-05-27 06:38

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0040_page_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='created',
            field=models.DateField(auto_now_add=True, default='2020-09-19'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contacts',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='phone1',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='page',
            name='phone2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
