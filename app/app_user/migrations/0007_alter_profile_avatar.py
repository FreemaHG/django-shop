# Generated by Django 4.1.3 on 2023-06-03 11:54

import app_user.utils.models.saving_files
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0006_buyer_deleted_profile_deleted_seller_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=app_user.utils.models.saving_files.save_avatar, verbose_name='Аватар'),
        ),
    ]