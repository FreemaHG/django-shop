import logging

from typing import Union, Dict
from django.db.models import QuerySet

from ...models import Product


logger = logging.getLogger(__name__)

class ProductSorted:
    """
    Сервис с бизнес-логикой по сортировке товаров по популярности, цене, отзывам и новизне
    """

    # Переключатели для сортировки со значениями по умолчанию
    # FIXME Флаги учитываются (меняются) для разных сессий (пользователей)
    # popularity_up = True
    # price_up = True
    # reviews_up = True
    # novelty_up = True

    # FIXME доделать после реализации механизма покупок
    @classmethod
    def by_popularity_up(cls):
        """
        Сортировка товаров по популярности (кол-ву покупок) (по возрастанию)
        """
        ...

    # FIXME доделать после реализации механизма покупок
    @classmethod
    def by_popularity_down(cls):
        """
        Сортировка товаров по популярности (кол-ву покупок) (по убыванию)
        """
        ...

    # FIXME Смена флага сортировки для текущей сессии пользователя
    @classmethod
    def by_price_up(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по цене (по возрастанию)
        """
        logger.debug('Сортировка по цене (по возрастанию)')
        sorted_products = products.order_by('price')
        # cls.price_up = False  # Меняем флаг
        logger.debug(f'Отсортированные товары: {sorted_products}')

        return sorted_products

    @classmethod
    def by_price_down(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по цене (по убыванию)
        """
        logger.debug('Сортировка по цене (по убыванию)')
        sorted_products = products.order_by('-price')
        # cls.price_up = True  # Меняем флаг
        logger.debug(f'Отсортированные товары: {sorted_products}')

        return sorted_products

    @classmethod
    def by_reviews_up(cls):
        """
        Сортировка товаров по отзывам (их кол-ву) (по возрастанию)
        """
        ...

    @classmethod
    def by_reviews_down(cls):
        """
        Сортировка товаров по отзывам (их кол-ву) (по убыванию)
        """
        ...

    @classmethod
    def by_novelty_up(cls):
        """
        Сортировка товаров по новизне (дате публикации товара) (по возрастанию)
        """
        ...

    @classmethod
    def by_novelty_down(cls):
        """
        Сортировка товаров по новизне (дате публикации товара) (по убыванию)
        """
        ...
