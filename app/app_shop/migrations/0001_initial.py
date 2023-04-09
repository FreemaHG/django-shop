# Generated by Django 4.1.3 on 2023-03-28 20:30

import app_shop.utils.models.saving_files
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(max_length=100, verbose_name='URL')),
                ('icon', models.ImageField(blank=True, upload_to=app_shop.utils.models.saving_files.saving_the_category_icon, verbose_name='Иконка')),
                ('image', models.ImageField(blank=True, upload_to=app_shop.utils.models.saving_files.saving_the_category_image, verbose_name='Изображение')),
                ('selected', models.BooleanField(default=False, verbose_name='Избранная категория')),
                ('deleted', models.BooleanField(choices=[(True, 'Удалено'), (False, 'Активно')], default=False, verbose_name='Статус')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app_shop.categoryproduct', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'db_table': 'categories_products',
            },
        ),
    ]
