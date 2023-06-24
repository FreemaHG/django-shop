import logging
import random

from typing import Tuple
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from ..models.cart_and_orders import Order, PaymentErrors


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
        logger.info(f'Запуск обработки оплаты заказа')

        order = PaymentService.check_order(order_id=order_id)

        # Убираем пробелы и преобразуем в число
        cart_number = int(cart_number.replace(' ', ''))

        if not order is False:
            order.status=3  # Смена статуса заказа на "Подтверждение оплаты"
            order.save()
            res = PaymentService.payment(order=order, cart_number=cart_number)  # Прямой вызов метода
            # payment(order=order, cart_number=cart_number)  # Добавление оплаты в очередь задач

            return res

        else:
            return False


    @classmethod
    def check_order(cls, order_id: int) -> Tuple[Order, bool]:
        """
        Метод для поиска заказа по переданному номеру

        @param order_id: id заказа
        @return: объект заказа / False, если заказ не найден
        """
        logger.debug(f'Поиск заказа №{order_id}')

        try:
            order = Order.objects.get(id=order_id)
            logger.debug(f'Заказ №{order_id} найден')
            return order

        except ObjectDoesNotExist:
            logger.error('Заказ не найден')
            return False


    @classmethod
    @transaction.atomic
    def payment(cls, order: Order, cart_number: int) -> bool:
        """
        Метод оплаты заказа

        @param order: объект заказа
        @param cart_number: номер карты
        @return: bool-значение
        """
        logger.info(f'Оплата заказа: №{order.id}, карта №{cart_number}, сумма к оплате - {order.order_cost} руб')

        if order:
            if cart_number % 2 == 0 and cart_number % 10 != 0:
                order.status = 4  # Смена статуса заказа на "Оплачен"
                order.error_message = None  # Удаляем сообщение ошибки, если оно было
                order.save()
                logger.info(f'Заказ #{order.id} успешно оплачен')

                return True

            else:
                order.status = 2  # Смена статуса заказа на "Не оплачен"
                errors_count = PaymentErrors.objects.count()
                random_error_message = PaymentErrors.objects.get(id=random.randint(1, errors_count - 1))
                order.error_message = random_error_message
                order.save()

                logger.error(f'Заказ #{order.id} не оплачен. Ошибка: "{random_error_message.title}"')

                return False

        else:
            return False
