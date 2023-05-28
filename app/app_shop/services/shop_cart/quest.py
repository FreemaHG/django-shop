import logging

from typing import List
from django.db.models import Sum
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ...models import Cart, Product


logger = logging.getLogger(__name__)

class ProductsCartQuestService:
    """
    Сервис для добавления, изменения и удаления товаров из корзины (session)
    """
    ...
    @classmethod
    def add(cls, user: User, product_id: int, count: int = 1) -> bool:
        """
        Добавить товар в корзину
        """
        ...

    @classmethod
    def remove(cls, user: User, product_id: int):
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
    def check(cls, user: User, product: Product) -> bool:
        """
        Проверка, есть ли указанный товар в корзине текущего пользователя
        """
        ...

    @classmethod
    def all(cls, user: User):
        """
        Вывести все товары в корзине для текущего пользователя
        """
        ...

    @classmethod
    def total_cost(cls, products: List[Cart]):
        """
        Возврат общей стоимости всех товаров в корзине
        """
        ...
