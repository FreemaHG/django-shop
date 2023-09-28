import logging

from typing import Dict
from django.contrib.auth.models import User
from django.db import models

from app.app_shop.models.products import Product


logger = logging.getLogger(__name__)


class Cart(models.Model):
    """
    Модель для хранения данных о корзине пользователя с товарами
    """

    # Warning null=True нужно исключительно для создания экземпляра корзины для анонимного пользователя из данных сессии
    # с последующей передачей данных в шаблон, чтобы не делать новую верстку под корзину неавторизованного пользователя
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, verbose_name="Покупатель"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    count = models.PositiveIntegerField(default=1, verbose_name="Кол-во")

    class Meta:
        db_table = "products_cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self) -> str:
        return f"Корзина покупателя"

    @property
    def position_cost(self) -> int:
        """
        Стоимость одной позиции товара с учетом скидки и кол-ва товара (с округлением до целого)
        """
        product = self.product
        price = product.price

        return int((price - (price * (product.discount / 100))) * self.count)


class PaymentErrors(models.Model):
    """
    Модель для хранения возможных сообщений об ошибках при оплате заказа
    """

    title = models.CharField(max_length=150, verbose_name="Сообщение ошибки")
    description = models.CharField(max_length=500, verbose_name="Описание ошибки")

    class Meta:
        db_table = "payment_errors"
        verbose_name = "Ошибка оплаты"
        verbose_name_plural = "Ошибки оплаты"

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    """
    Модель для хранения данных о заказах
    """

    STATUS_CHOICES = (
        (1, "Оформлен"),
        (2, "Не оплачен"),
        (3, "Подтверждение оплаты"),
        (4, "Оплачен"),
        (5, "Доставляется"),
    )

    DELIVERY_CHOICES = (
        (1, "Обычная доставка"),
        (2, "Экспресс доставка"),
    )

    PAYMENT_CHOICES = (
        (1, "Онлайн картой"),
        (2, "Онлайн со случайного чужого счета"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    data_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оформления заказа"
    )
    city = models.CharField(max_length=100, null=True, verbose_name="Город")
    address = models.CharField(max_length=500, null=True, verbose_name="Адрес доставки")
    delivery = models.IntegerField(
        choices=DELIVERY_CHOICES, default=1, verbose_name="Тип доставки"
    )
    payment = models.IntegerField(
        choices=PAYMENT_CHOICES, default=1, verbose_name="Оплата"
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name="Статус"
    )
    error_message = models.ForeignKey(
        PaymentErrors,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сообщение об ошибке",
    )

    @property
    def order_cost(self) -> Dict:
        """
        Расчет стоимости заказа с учетом кол-ва каждого товара и текущей цены с учетом скидки
        """
        products = PurchasedProduct.objects.filter(order__id=self.id)
        amount = sum(record.price for record in products)

        return amount

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-data_created"]

    def __str__(self) -> str:
        return f"Заказ №{self.id}"


class PurchasedProduct(models.Model):
    """
    Модель для хранения товаров, их кол-ва и стоимости на момент покупки с привязкой к номеру заказа
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Номер заказа"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Наименование товара"
    )
    count = models.PositiveIntegerField(verbose_name="Кол-во")
    price = models.PositiveIntegerField(
        verbose_name="Цена"
    )  # Берется из корзины с учетом скидки!

    class Meta:
        db_table = "purchased_products"
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self) -> str:
        return self.product.name

    @property
    def position_cost(self) -> int:
        """
        Стоимость одной позиции товара с кол-ва (с округлением до целого)
        """
        return int(self.price * self.count)
