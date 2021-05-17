# Generated by Django 3.2.2 on 2021-05-17 18:41

import creditcards.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210516_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=40, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cc_number',
            field=creditcards.models.CardNumberField(max_length=25, verbose_name='Номер карты'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(choices=[('ODESSA', 'Одесса'), ('KIEV', 'Киев'), ('KHARKIV', 'Харьков')], default='ODESSA', max_length=20, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=20, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(max_length=40, verbose_name='Полное имя'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужчина'), ('F', 'Женщина')], default='M', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(choices=[('EN', 'Английский'), ('RU', 'Русский')], default='RU', max_length=2, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=20, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=20, unique=True, verbose_name='Никнейм'),
        ),
    ]
