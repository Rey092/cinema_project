# Generated by Django 3.2.2 on 2021-06-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_site', '0053_alter_emailtemplate_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='file',
            field=models.FileField(upload_to='email_template/'),
        ),
    ]