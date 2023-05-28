import logging

from typing import List
from django.db.models import Sum
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ...models import Cart, Product
from .authenticated import ProductsCartUserService
from .quest import ProductsCartQuestService


logger = logging.getLogger(__name__)


class CartProductsListService:
    """
    Вывод товаров текущего пользователя: из БД для авторизованного / из объекта сессии для гостя
    """
    @classmethod
    def output(cls, request: HttpRequest):
        logger.debug('Сервис: вывод корзины с товарами')
        user = request.user

        if user.is_authenticated:
            logger.info('Пользователь авторизован')
            products = ProductsCartUserService.all(user=user)
        else:
            logger.info('Пользователь НЕ авторизован')
            ...

        return products


class CartProductsAddService:
    """
    Добавление и удаление товара из корзины.
    Вызов методов в зависимости от того, авторизован пользователь или нет.
    """

    @classmethod
    def add(cls, request: HttpRequest, product_id: int = None, count: int = 1):
        """
        Добавление товара в корзину
        """
        if not product_id:
            logger.warning('id товара не передан в качестве аргумента функции')
            product_id = int(request.GET.get('product_id'))
            count = int(request.GET.get('count', 1))

        logger.info(f'id товара: {product_id}, кол-во: {count}')

        if request.user.is_authenticated:
            # Добавление товара в корзину зарегистрированного пользователя
            res = ProductsCartUserService.add(user=request.user, product_id=product_id, count=count)
        else:
            # Добавление товара в корзину гостя (запись в объект сессии)
            res = ProductsCartQuestService.add(user=request.user, product_id=product_id, count=count)

        return res

    @classmethod
    def delete(cls, request: HttpRequest, product_id: int):
        """
        Удаление товара из корзины
        """
        if request.user.is_authenticated:
            # Добавление товара в корзину зарегистрированного пользователя
            res = ProductsCartUserService.remove(user=request.user, product_id=product_id)
        else:
            # Добавление товара в корзину гостя (запись в объект сессии)
            res = ProductsCartQuestService.remove(user=request.user, product_id=product_id)

        return res
