# Generated by Django 4.1.3 on 2023-06-07 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_shop', '0018_alter_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('address', models.CharField(max_length=500, verbose_name='Адрес')),
                ('delivery', models.IntegerField(choices=[(1, 'Обычная доставка'), (2, 'Экспресс доставка')], default=1, verbose_name='Тип доставки')),
                ('payment', models.IntegerField(choices=[(1, 'Онлайн картой'), (2, 'Онлайн со случайного чужого счета')], default=1, verbose_name='Оплата')),
                ('status', models.IntegerField(choices=[(1, 'Не оплачен'), (2, 'Подтверждение оплаты'), (3, 'Оплачен'), (4, 'Доставляется')], default=1, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentErrors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Сообщение ошибки')),
                ('description', models.CharField(max_length=500, verbose_name='Описание ошибки')),
            ],
            options={
                'verbose_name': 'Ошибка оплаты',
                'verbose_name_plural': 'Ошибки оплаты',
                'db_table': 'payment_errors',
            },
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(verbose_name='Кол-во товара')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'История покупок',
                'verbose_name_plural': 'История покупок',
                'db_table': 'purchased_products',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='error_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_shop.paymenterrors', verbose_name='Сообщение об ошибке'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
    ]