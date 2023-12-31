# Generated by Django 4.1.3 on 2023-04-29 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("config", "0002_siteconfiguration_extra_shipping_cost_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteconfiguration",
            name="extra_shipping_cost",
            field=models.IntegerField(
                default=500,
                verbose_name="Надбавочная стоимость для экспресс-доставки (руб.)",
            ),
        ),
        migrations.AlterField(
            model_name="siteconfiguration",
            name="min_order_cost",
            field=models.IntegerField(
                default=2000,
                verbose_name="Минимальная стоимость заказа для бесплатной доставки (руб.)",
            ),
        ),
        migrations.AlterField(
            model_name="siteconfiguration",
            name="shipping_cost",
            field=models.IntegerField(
                default=200, verbose_name="Стоимость обычной доставки (руб.)"
            ),
        ),
    ]
