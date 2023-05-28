import logging

from typing import List
from django.db.models import Sum
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ...models import Cart, Product


logger = logging.getLogger(__name__)

class ProductsCartUserService:
    """
    Сервис для добавления, изменения и удаления товаров из корзины (БД)
    """

    @classmethod
    def add(cls, user: User, product_id: int, count: int = 1) -> bool:
        """
        Добавить товар в корзину
        """
        logger.debug(f'Добавление товара в корзину: user: {user.profile.full_name}, id - {product_id}, кол-во: {count}')

        product = Product.objects.get(id=product_id)
        logger.info(f'Товар найден: {product.name}')

        if count == 0:
            logger.warning('Нельзя добавить 0 товаров, увеличение кол-ва на 1')
            count = 1

        if ProductsCartUserService.check(user=user, product_id=product_id):
            logger.warning('Добавляемый товар уже есть в корзине пользователя')
            ProductsCartUserService.change_quantity(user=user, product_id=product_id, count=count)
        else:
            Cart.objects.create(user=user, product=product, count=count)

        return True

    @classmethod
    def remove(cls, user: User, product_id: int) -> bool:
        """
        Удалить товар из корзины
        """
        logger.debug(f'Удаление товара из корзины: user: {user.profile.full_name}, id - {product_id}')
        Cart.objects.filter(user=user, product__id=product_id).delete()

        return True

    @classmethod
    def change_quantity(cls, user: User, product_id: int, count: int):
        """
        Изменить кол-во товара в корзине
        """
        logger.debug('Изменение кол-ва товара в корзине')
        logger.debug(f'Изменить кол-во на: {count}')

        # FIXME Обработать ошибку, если товаров несколько!
        record = Cart.objects.get(user=user, product__id=product_id)
        logger.info(f'Товар: id - {product_id}, кол-во (было): {record.count}')

        record.count += count

        if record.count <= 0:
            logger.warning('Кол-во товара меньше или равно 0. Удаление товара из корзины')
            ProductsCartUserService.remove(user=user, product_id=product_id)
        else:
            record.save()
            logger.info(f'Товар: id - {product_id}, кол-во (стало): {record.count}')

    @classmethod
    def check(cls, user: User, product_id: int) -> bool:
        """
        Проверка, есть ли указанный товар в корзине текущего пользователя
        """
        logger.debug('Проверка товара в корзине текущего пользователя')

        try:
            # FIXME Ошибка,если несколько одинаковых товаров
            Cart.objects.get(user=user, product__id=product_id)
            logger.info('Товар есть в корзине')
            return True

        except ObjectDoesNotExist:
            logger.info('Товара нет в корзине')
            return False

    @classmethod
    def all(cls, user: User):
        """
        Вывести все товары в корзине для текущего пользователя
        """
        logger.debug(f'Вывод товаров для покупателя: {user.profile.full_name}')
        products = Cart.objects.filter(user=user)

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
