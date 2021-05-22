# Generated by Django 3.2.2 on 2021-05-20 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_poster', to='cinema_site.image'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('video_url', models.URLField()),
                ('is_active', models.BooleanField()),
                ('mode', models.CharField(choices=[('NEWS', 'Новость'), ('EVENT', 'Акция')], max_length=5, verbose_name='Тип статьи')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_banner', to='cinema_site.image')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_seo', to='cinema_site.seodata')),
            ],
        ),
    ]
