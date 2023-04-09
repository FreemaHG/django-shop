# Generated by Django 4.1.3 on 2023-04-02 10:44

import app_user.utils.models.saving_files
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=150, verbose_name='ФИО')),
                ('phone_number', models.CharField(blank=True, max_length=10, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('avatar', models.ImageField(blank=True, upload_to=app_user.utils.models.saving_files.save_avatar, verbose_name='Аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профайл',
                'verbose_name_plural': 'Профайлы',
                'db_table': 'profile',
            },
        ),
    ]