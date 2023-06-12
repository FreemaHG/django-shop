import logging
import random

from typing import List

from django.db import transaction
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist

from ..services.shop_cart.authenticated import ProductsCartUserService
from ..models import PurchasedProduct, Cart, Order, PaymentErrors
from ..forms import MakingOrderForm


logger = logging.getLogger(__name__)

class Payment:
    """
    Сервис для оплаты получения статуса заказов
    """

    @classmethod
    def payment_processing(cls, order_id: int, cart_number: int):
        """
        Обработка оплаты заказа
        """
        logger.info(f'Запуск обработки оплаты заказа')
        order = Payment.check_order(order_id=order_id)

        # TODO Добавить задержку в несколько сек

        if not order is False:
            order.status=3  # Смена статуса заказа на "Подтверждение оплаты"
            order.save()
            Payment.payment(order=order, cart_number=cart_number)
        else:
            return False


    @classmethod
    def check_order(cls, order_id: int):
        """
        Метод для поиска заказа по переданному номеру
        """
        logger.debug(f'Поиск заказа #{order_id}')

        try:
            order = Order.objects.get(id=order_id)
            logger.debug(f'Заказ #{order_id} найден')
            return order
        except ObjectDoesNotExist:
            logger.error('Заказ не найден')
            return False

    @classmethod
    def payment(cls, order: Order, cart_number: int):
        """
        Метод оплаты заказа
        """
        logger.info(f'Оплата заказа: №{order.id}, карта №{cart_number}, сумма к оплате - {order.order_cost} руб')

        if order:
            # TODO Проверка отсюда!!!
            if cart_number % 2 == 0 and cart_number // 10000 != 0:
                order.status=4  # Смена статуса заказа на "Оплачен"
                order.save()
                logger.info(f'Заказ #{order.id} успешно оплачен')
            else:
                order.status = 2  # Смена статуса заказа на "Не оплачен"
                errors_count = PaymentErrors.objects.count()
                random_error_message = PaymentErrors.objects.get(id=random.randint(1, errors_count - 1))
                order.error_message = random_error_message
                order.save()

                logger.error(f'Заказ #{order.id} не оплачен. Ошибка: {random_error_message.title}')
        else:
            return False

    @classmethod
    def order_payment_status(cls, order_id: int):
        """
        Метод для получения статуса оплаты заказа
        """
        ...
