# Generated by Django 3.2.2 on 2021-06-14 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema_site', '0058_alter_page_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.gallery'),
        ),
        migrations.AlterField(
            model_name='article',
            name='seo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_seo', to='cinema_site.seodata'),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.gallery'),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='seo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.seodata'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='cinema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hall_cinema', to='cinema_site.cinema'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.gallery'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='seo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hall_seo', to='cinema_site.seodata'),
        ),
        migrations.AlterField(
            model_name='image',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.gallery'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.gallery'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='seo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_seo', to='cinema_site.seodata'),
        ),
        migrations.AlterField(
            model_name='page',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema_site.gallery'),
        ),
        migrations.AlterField(
            model_name='page',
            name='seo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_seo', to='cinema_site.seodata'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='hall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seance_hall', to='cinema_site.hall'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seance_movie', to='cinema_site.movie'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_seance', to='cinema_site.seance'),
        ),
    ]
