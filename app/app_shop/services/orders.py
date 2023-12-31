import logging

from typing import List, Dict
from django.core.cache import cache
from django.db import transaction
from django.http import HttpRequest

from app.config.utils.configuration import get_config
from app.app_shop.services.shop_cart.authenticated import ProductsCartUserService
from app.app_shop.models.cart_and_orders import PurchasedProduct, Cart, Order
from app.app_shop.forms import MakingOrderForm


logger = logging.getLogger(__name__)


class RegistrationOrderService:
    """
    Сервис для оформления заказа
    """

    @classmethod
    @transaction.atomic
    def create_order(cls, request: HttpRequest, form: MakingOrderForm) -> Order:
        """
        Метод для регистрации нового заказа

        @param request: объект http-запроса
        @param form: объект формы с данными заказа
        @return: объект созданного заказа
        """
        logger.debug("Создание заказа")

        delivery = form.cleaned_data.get("delivery", False)
        city = form.cleaned_data.get("city", False)
        address = form.cleaned_data.get("address", False)
        pay = form.cleaned_data.get("pay", False)

        if delivery == "ordinary":
            logger.debug("Доставка: обычная")
            delivery_num = 1
        else:
            logger.debug("Доставка: экспресс")
            delivery_num = 2

        if pay == "online":
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
            status=1,  # Оформлен
        )

        # Сохранение товаров заказа
        products_cart = ProductsCartUserService.all(user=request.user)
        RegistrationOrderService.purchase_history(
            products_cart=products_cart, order=order
        )

        # Очистка корзины
        ProductsCartUserService.clear_cart(user=request.user)

        # Стоимость оплаты = стоимость товаров + стоимость доставки
        amount = order.order_cost + RegistrationOrderService.delivery_cost(order=order)
        logger.debug(f"Стоимость заказа с учетом доставки: {amount} руб")

        return order

    @classmethod
    def purchase_history(cls, products_cart: List[Cart], order: Order) -> None:
        """
        Метод для сохранения товаров заказа

        @param products_cart: список с позициями товаров в заказе (товар и его кол-во)
        @param order: объект заказа
        @return: None
        """
        logger.debug("Сохранение товаров в заказе")

        purchase_products = [
            PurchasedProduct(
                order=order,
                product=record.product,
                count=record.count,
                price=record.position_cost,  # Стоимость товара * кол-во (с учетом скидки)
            )
            for record in products_cart
        ]

        PurchasedProduct.objects.bulk_create(purchase_products)

    @classmethod
    def delivery_cost(cls, order: Order) -> int:
        """
        Метод для расчета стоимости доставки заказа:
            - Обычная: если сумма заказа > 2000 - доставка 0 руб, иначе 200 (стоимость обычной доставки);
            - Экспресс: если сумма заказа > 2000 - доставка 500 (стоимость экспресс доставки), иначе 700 (200 + 500).

        @param order: объект заказа
        @return: стоимость доставки
        """
        logger.debug("Расчет стоимости доставки")

        config = get_config()

        # Обычная доставка
        if order.delivery == 1:
            if order.order_cost > config.min_order_cost:
                delivery_cost = 0
            else:
                delivery_cost = config.shipping_cost

            logger.debug(f"Обычная доставка. Стоимость: {delivery_cost} руб")

            return delivery_cost

        # Экспресс доставка
        else:
            if order.order_cost > config.min_order_cost:
                delivery_cost = config.extra_shipping_cost
            else:
                delivery_cost = config.shipping_cost + config.extra_shipping_cost

            logger.debug(f"Экспресс доставка. Стоимость: {delivery_cost} руб")

            return delivery_cost

    @classmethod
    def last_order(cls, request: HttpRequest) -> Order:
        """
        Метод для возврата последнего заказа пользователя

        @param request: объект http-запроса
        @return: объект последнего заказа текущего пользователя
        """
        logger.debug(
            f"Возврат последнего заказа для пользователя: {request.user.profile.full_name}"
        )

        # По умолчанию у заказов обратная сортировка по дате создания,
        # поэтому для возврата последнего заказа используем first()
        return Order.objects.filter(user=request.user).first()

    @classmethod
    def save_order_products_in_context(cls, context: Dict, order: Order) -> Dict:
        """
        Метод сохраняет в переменную контекста товары текущего заказа

        @param context: словарь - контекстная переменная представления
        @param order: объект заказа
        @return: словарь - контекстная переменная представления с сохраненными данными по товарам
        """
        logger.debug(f"Сохранение в контексте товаров заказа №{order.id}")

        config = get_config()

        products = cache.get_or_set(
            f"order_{order.id}",
            PurchasedProduct.objects.select_related("product")
            .only(
                "id",
                "count",
                "price",
                "product__id",
                "product__name",
                "product__price",
                "product__definition",
            )
            .filter(order=order),
            60 * config.caching_time,
        )

        context["products"] = products

        return context
