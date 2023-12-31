# Generated by Django 4.1.3 on 2023-05-18 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_shop", "0013_alter_cart_options_remove_cart_product_cart_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="product",
        ),
        migrations.AddField(
            model_name="cart",
            name="product",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="app_shop.product",
                verbose_name="Товар",
            ),
            preserve_default=False,
        ),
    ]
