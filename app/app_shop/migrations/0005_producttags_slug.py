# Generated by Django 4.1.3 on 2023-04-29 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_shop", "0004_alter_product_characteristics_alter_product_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="producttags",
            name="slug",
            field=models.SlugField(default="", max_length=100, verbose_name="URL"),
        ),
    ]
