import logging
import random
import time

from celery import shared_task

from app.app_shop.models.cart_and_orders import PaymentErrors, Order

logger = logging.getLogger(__name__)


@shared_task()
def payment(order_id: int, cart_number: int) -> bool:
    """
    Оплата заказа

    @param order: объект заказа
    @param cart_number: номер карты
    @return: True - успешно, иначе False
    """

    # Поиск заказа по id
    order = Order.objects.get(id=order_id)

    if not order is False:
        logger.info(
            f"Оплата заказа: №{order_id}, карта №{cart_number}, сумма к оплате - {order.order_cost} руб"
        )

        order.status = 3  # Смена статуса заказа на "Подтверждение оплаты"
        order.save()

        # Имитация ожидания оплаты заказа
        time.sleep(10)

        if cart_number % 2 == 0 and cart_number % 10 != 0:
            order.status = 4  # Смена статуса заказа на "Оплачен"
            order.error_message = None  # Удаляем сообщение ошибки, если оно было
            order.save()
            logger.info(f"Заказ #{order.id} успешно оплачен")

            return True

        else:
            order.status = 2  # Смена статуса заказа на "Не оплачен"
            errors_count = PaymentErrors.objects.count()
            random_error_message = PaymentErrors.objects.get(
                id=random.randint(1, errors_count - 1)
            )
            order.error_message = random_error_message
            order.save()

            logger.error(
                f'Заказ #{order.id} не оплачен. Ошибка: "{random_error_message.title}"'
            )

            return False
    else:
        logger.error(f"Заказ №{order_id} не найден!")

        return False
