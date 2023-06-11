import logging

from typing import List

from django.db import transaction
from django.http import HttpRequest

from config.admin import config
from ..services.shop_cart.authenticated import ProductsCartUserService
from ..services.orders_payment import Payment
from ..models import PurchasedProduct, Cart, Order
from ..forms import MakingOrderForm


logger = logging.getLogger(__name__)


class RegistrationOrder:
    """
    Сервис для оформления заказа
    """
    @classmethod
    @transaction.atomic
    def create_order(cls, request: HttpRequest, form: MakingOrderForm) -> Order:
        """
        Создание заказа
        """
        logger.debug('Создание заказа')
        # full_name = form.cleaned_data.get('full_name', False)
        # phone_number = form.cleaned_data.get('phone_number', False)
        # email = form.cleaned_data.get('email', False)
        delivery = form.cleaned_data.get('delivery', False)
        city = form.cleaned_data.get('city', False)
        address = form.cleaned_data.get('address', False)
        pay = form.cleaned_data.get('pay', False)

        if delivery == 'ordinary':
            logger.debug('Доставка: обычная')
            delivery_num = 1
        else:
            logger.debug('Доставка: экспресс')
            delivery_num = 2

        if pay == 'online':
            logger.debug('Оплата "Онлайн картой"')
            pay_num = 1
        else:
            logger.debug('Оплата "Онлайн со случайного чужого счета"')
            pay_num = 2

        order = Order.objects.create(
            user=request.user,
            city=city,
            address=address,
            delivery=delivery_num,
            payment=pay_num,
            status=1  # Оформлен
        )

        # Сохранение товаров заказа
        products_cart = ProductsCartUserService.all(user=request.user)
        RegistrationOrder.purchase_history(products_cart=products_cart, order=order)

        # Очистка корзины
        ProductsCartUserService.clear_cart(user=request.user)

        # FIXME Тестовое значение. Изменить на введенное пользователем значение!!!
        cart_number = 12345678

        # Стоимость оплаты = стоимость товаров + стоимость доставки
        amount = order.order_cost + RegistrationOrder.delivery_cost(order=order)
        logger.debug(f'Стоимость заказа с учетом доставки: {amount} руб')

        return order

    @classmethod
    def purchase_history(cls, products_cart: List[Cart], order: MakingOrderForm):
        """
        Метод для сохранения товаров заказа
        """
        logger.debug('Сохранение товаров в заказе')

        purchase_products = [
            PurchasedProduct(
                order=order,
                product=record.product,
                count=record.count,
                price=record.position_cost  # Стоимость товара * кол-во (с учетом скидки)
            )
            for record in products_cart
        ]

        PurchasedProduct.objects.bulk_create(purchase_products)

    @classmethod
    def delivery_cost(cls, order: Order):
        """
        Метод для расчета стоимости доставки заказа:
            - Обычная: если сумма заказа > 2000 - доставка 0 руб, иначе 200 (стоимость обычной доставки);
            - Экспресс: если сумма заказа > 2000 - доставка 500 (стоимость экспресс доставки), иначе 700 (200 + 500).
        """
        logger.debug('Расчет стоимости доставки')

        # Обычная доставка
        if order.delivery == 1:
            if order.order_cost > config.min_order_cost:
                delivery_cost = 0
            else:
                delivery_cost = config.shipping_cost

            logger.debug(f'Обычная доставка. Стоимость: {delivery_cost} руб')
            return delivery_cost

        # Экспресс доставка
        else:
            if order.order_cost > config.min_order_cost:
                delivery_cost = config.extra_shipping_cost
            else:
                delivery_cost = config.shipping_cost + config.extra_shipping_cost

            logger.debug(f'Экспресс доставка. Стоимость: {delivery_cost} руб')
            return delivery_cost
