import logging

from typing import List

from django.db import transaction
from django.http import HttpRequest

from ..services.shop_cart.authenticated import ProductsCartUserService
from ..models import PurchasedProduct, Cart
from ..forms import MakingOrderForm


logger = logging.getLogger(__name__)

class Payment:
    """
    Сервис для оплаты получения статуса заказов
    """

    @classmethod
    def payment(cls, order_id: int, cart_number: int, amount: int):
        """
        Метод оплаты заказа
        """
        logger.info(f'Запуск сервиса по оплате заказа: заказ №{order_id}, карта №{cart_number}, сумма к оплате - {amount} руб')
        ...

    @classmethod
    def order_payment_status(cls, order_id: int):
        """
        Метод для получения статуса заказа
        """
        ...