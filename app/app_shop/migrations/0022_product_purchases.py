# Generated by Django 4.1.3 on 2023-06-14 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0021_alter_order_options_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='purchases',
            field=models.PositiveIntegerField(default=0, verbose_name='Покупок'),
        ),
    ]