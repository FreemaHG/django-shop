# Generated by Django 4.1.3 on 2023-06-11 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0019_order_paymenterrors_purchasedproduct_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='purchasedproduct',
            options={'verbose_name': 'Товар в заказе', 'verbose_name_plural': 'Товары в заказе'},
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=500, null=True, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=100, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='order',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Оформление'), (2, 'Не оплачен'), (3, 'Подтверждение оплаты'), (4, 'Оплачен'), (5, 'Доставляется')], default=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='purchasedproduct',
            name='count',
            field=models.PositiveIntegerField(verbose_name='Кол-во'),
        ),
        migrations.AlterField(
            model_name='purchasedproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.order', verbose_name='Номер заказа'),
        ),
        migrations.AlterField(
            model_name='purchasedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_shop.product', verbose_name='Наименование товара'),
        ),
    ]