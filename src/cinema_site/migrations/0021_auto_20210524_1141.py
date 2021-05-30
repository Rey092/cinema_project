# Generated by Django 3.2.2 on 2021-05-24 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0020_alter_movie_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='hall',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema_site.gallery'),
        ),
        migrations.AddField(
            model_name='movie',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema_site.gallery'),
        ),
    ]