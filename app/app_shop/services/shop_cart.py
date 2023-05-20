import logging

from typing import List
from django.db.models import Sum
from django.http import HttpRequest

from app_user.utils.models.buyer import BuyerUtils
from app_user.utils.models.profile import ProfileUtils
from app_user.models import Buyer
from ..models import Cart


logger = logging.getLogger(__name__)


class CartProductsListService:
    """
    Вывод товаров текущего пользователя: из БД для авторизованного / из сессии для неавторизованного
    """
    @classmethod
    def output(cls, request: HttpRequest):
        logger.debug('Сервис: вывод корзины с товарами')

        user = request.user

        if user.is_authenticated:
            profile = ProfileUtils.get(user=user)

            if profile:
                buyer = BuyerUtils.get(profile=profile)

                if buyer:
                    products = Products.all(buyer=buyer)

                    return products


class Products:
    """
    Сервис для добавления, изменения и удаления товаров из корзины
    """

    def add(self):
        """
        Добавить товар в корзину
        """
        ...

    def remove(self):
        """
        Удалить товар из корзины
        """
        ...

    def change_quantity(self):
        """
        Изменить кол-во товара в корзине
        """
        ...

    @classmethod
    def all(cls, buyer: Buyer):
        """
        Вывести все товары в корзине для текущего пользователя
        """
        logger.debug(f'Вывод товаров для покупателя: {buyer.profile.full_name}')
        products = Cart.objects.filter(buyer=buyer)

        return products

    def count(self):
        """
        Вывести кол-во товара в корзине
        """
        ...

    @classmethod
    def total_cost(cls, products: List[Cart]):
        """
        Возврат общей стоимости всех товаров в корзине
        """
        logger.debug('Подсчет общей стоимости товаров в корзине')
        total_cost = sum(product.position_cost for product in products)

        return total_cost