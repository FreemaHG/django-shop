import logging
import random
import time

from typing import Tuple
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from app.app_shop.models.cart_and_orders import Order, PaymentErrors
from app.app_shop.tasks import payment


logger = logging.getLogger(__name__)


class PaymentService:
    """
    Сервис для оплаты получения статуса заказов
    """

    @classmethod
    def payment_processing(cls, order_id: int, cart_number: str) -> bool:
        """
        Метод для оплаты заказа

        @param order_id: id заказа
        @param cart_number: номер карты в виде строки
        @return: bool-значение
        """
        logger.info(f"Запуск обработки оплаты заказа")

        # Убираем пробелы и преобразуем в число
        cart_number = int(cart_number.replace(" ", ""))

        # Оплата заказа в фоне через Celery
        # После навешивания декоратора @shared_task() на функцию оплаты становится доступным метод delay
        # для передачи сообщения о задаче в Celery
        res = payment.delay(order_id=order_id, cart_number=cart_number)

        return res

    @classmethod
    def check_order(cls, order_id: int) -> Tuple[Order, bool]:
        """
        Метод для поиска заказа по переданному номеру

        @param order_id: id заказа
        @return: объект заказа / False, если заказ не найден
        """
        logger.debug(f"Поиск заказа №{order_id}")

        try:
            order = Order.objects.get(id=order_id)
            logger.debug(f"Заказ №{order_id} найден")
            return order

        except ObjectDoesNotExist:
            logger.error("Заказ не найден")
            return False
