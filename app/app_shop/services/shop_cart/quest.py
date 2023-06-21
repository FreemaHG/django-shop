import logging

from typing import List
from django.db.models import Sum
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ...models.products import Product
from ...models.cart_and_orders import Cart


logger = logging.getLogger(__name__)


# TODO Очищать кэш при изменении данных в корзине!!!
class ProductsCartQuestService:
    """
    Сервис для добавления, изменения и удаления товаров из корзины неавторизованного пользователя (session)
    """
    ...
    @classmethod
    def add(cls, request: HttpRequest, product_id: str, count: int = 1) -> bool:
        """
        Добавить товар в корзину
        """
        logger.debug(f'Добавление товара в корзину гостя: id пользователя: {request.user.id}, id - {product_id}, кол-во: {count}')
        ProductsCartQuestService.check_cart(request=request)  # Проверка / создание ключа "cart" в объекте сессии

        if count == 0:
            logger.warning('Нельзя добавить 0 товаров, увеличение кол-ва на 1')
            count = 1

        logger.debug(f'Корзина ДО: {request.session["cart"]}')

        record = request.session['cart'].get(product_id, False)

        if record:
            logger.warning('Товар уже есть в корзине, увеличение кол-ва')
            request.session['cart'][product_id] += count
        else:
            logger.info('Добавление нового товара')
            request.session['cart'][product_id] = count

        request.session.save()
        logger.debug(f'Корзина ПОСЛЕ: {request.session["cart"]}')

        return True


    @classmethod
    def remove(cls, request: HttpRequest, product_id: int) -> None:
        """
        Удалить товар из корзины
        """
        logger.debug(f'Удаление товара из объекта сессии: id = {product_id}')

        try:
            del request.session['cart'][product_id]
            request.session.save()
            logger.info('Товар удален из объекта сессии')

        except KeyError:
            logger.warning(f'Не найден ключ "cart" в объекте сессии гостя')


    @classmethod
    def reduce_product(cls, request: HttpRequest, product_id: int):
        """
        Уменьшение кол-ва товара на 1
        """
        product_id = str(product_id)
        count = request.session['cart'][product_id]
        count -= 1

        if count <= 0:
            logger.warning('Кол-во товара уменьшено до 0. Удаление товара из корзины')
            ProductsCartQuestService.remove(request=request, product_id=product_id)

        else:
            request.session['cart'][product_id] = count
            request.session.save()


    @classmethod
    def increase_product(cls, request: HttpRequest, product_id: int):
        """
        Увеличение кол-ва товара на 1
        """
        product_id = str(product_id)
        count = request.session['cart'][product_id]
        count += 1

        request.session['cart'][product_id] = count
        request.session.save()


    # FIXME Переименовать в check_key!!!
    @classmethod
    def check_cart(cls, request: HttpRequest):
        """
        Проверка ключа в объекте сессии (создание при необходимости) для записи, чтения и удаления товаров
        """
        logger.debug('Проверка ключа "cart" в объекте сессии текущего пользователя')

        if not request.session.get('cart', False):
            logger.warning('Ключ не найден, создание ключа')
            request.session['cart'] = {}

    # FIXME Возможно метод не нужен, перепроверить!
    @classmethod
    def check_product(cls, request: HttpRequest, product_id: int) -> bool:
        """
        Проверка, есть ли указанный товар в корзине текущего пользователя
        """
        logger.debug('Проверка товара в корзине гостя')
        ...

    @classmethod
    def all(cls, request: HttpRequest):
        """
        Вывести все товары в корзине для текущего пользователя
        """
        logger.debug(f'Вывод товаров корзины гостя: {request.user}')
        records_list = []

        products = request.session.get('cart', False)

        if products:
            logger.debug(f'Записи о товарах в объекте сессии гостя: {products}')

            for prod_id, count in products.items():
                records_list.append(Cart(
                    product=Product.objects.get(id=prod_id),
                    count=count
                ))
        else:
            logger.warning('Записи о товарах не найдены')

        return records_list

    # TODO Используется одноименный метод в ProductsCartUserService!
    @classmethod
    def total_cost(cls, products: List[Cart]):
        """
        Возврат общей стоимости всех товаров в корзине
        """
        ...
