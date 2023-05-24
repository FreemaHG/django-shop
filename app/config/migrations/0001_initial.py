# Generated by Django 4.1.3 on 2023-04-09 17:26

import config.utils.saving_fales
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(max_length=500, verbose_name='Описание')),
                ('site_url', models.URLField(max_length=150, null=True, verbose_name='URL')),
                ('logo_head', models.ImageField(upload_to=config.utils.saving_fales.saving_logo, verbose_name='Логотип в шапке')),
                ('logo_footer', models.ImageField(upload_to=config.utils.saving_fales.saving_logo, verbose_name='Логотип в футере')),
                ('maintenance_mode', models.BooleanField(default=False, verbose_name='Режим обслуживания')),
                ('selected_products', models.ManyToManyField(to='app_shop.categoryproduct', verbose_name='Избранные товары')),
            ],
            options={
                'verbose_name': 'Конфигурация сайта',
            },
        ),
    ]