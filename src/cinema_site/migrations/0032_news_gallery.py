# Generated by Django 3.2.2 on 2021-05-25 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0031_auto_20210525_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema_site.gallery'),
        ),
    ]
