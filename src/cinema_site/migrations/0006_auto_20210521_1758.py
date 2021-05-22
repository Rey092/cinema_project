# Generated by Django 3.2.2 on 2021-05-21 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0005_auto_20210521_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema_site.image')),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema_site.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='gallery',
            field=models.ManyToManyField(through='cinema_site.MovieGallery', to='cinema_site.Image'),
        ),
    ]
