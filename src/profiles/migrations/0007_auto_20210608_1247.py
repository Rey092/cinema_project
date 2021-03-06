# Generated by Django 3.2.2 on 2021-06-08 12:47

import creditcards.models
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_userprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cc_number',
            field=creditcards.models.CardNumberField(blank=True, max_length=25, null=True, verbose_name='Номер карты'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким именем пользователя уже существуют'}, help_text='Не более 20 символов. Только буквы и цифры.', max_length=20, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='Никнейм'),
        ),
    ]
