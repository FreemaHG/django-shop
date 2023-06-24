import logging

from typing import Dict
from django.db.models import QuerySet

from config.admin import config


logger = logging.getLogger(__name__)


class ProductFilterService:
    """
    Сервис по выводу отфильтрованных товаров
    """

    @classmethod
    def output(cls, products: QuerySet, filters: Dict) -> QuerySet:
        """
        Метод возвращает отфильтрованные товары по переданным параметрам

        @param products: QuerySet с товарами для фильтрации
        @param filters: словарь с параметрами фильтрации
        @return: QuerySet с отфильтрованными товарами
        """

        if filters:
            min_price = filters.get('min_price', False)
            max_price = filters.get('max_price', False)
            title = filters.get('title', False)
            in_stock = filters.get('in_stock', False)
            free_shipping = filters.get('free_shipping', False)

            if not min_price is False and min_price != '':
                products = cls.by_min_price(products=products, min_price=min_price)

            if not max_price is False and max_price != '':
                products = cls.by_max_price(products=products, max_price=max_price)

            if not title is False and title != '':
                products = cls.by_title(products=products, title=title)

            if not in_stock is False:
                products = cls.by_in_stock(products=products)

            if not free_shipping is False:
                products = cls.by_free_shipping(products=products)
        else:
            logger.warning('Параметры фильтрации не заданы')

        return products

    @classmethod
    def by_min_price(cls, products: QuerySet, min_price: str) -> QuerySet:
        """
        Метод для фильтрации товаров по минимальной цене

        @param products: QuerySet с товарами для фильтрации
        @param min_price: минимальное значение цены
        @return: QuerySet с отфильтрованными товарами
        """
        logger.debug(f'Фильтрация по минимальной цене: {min_price}')

        filtered_products =  products.filter(price__gte=min_price)
        logger.debug(f'Найдено товаров: {len(filtered_products)}')

        return filtered_products

    @classmethod
    def by_max_price(cls, products: QuerySet, max_price: str) -> QuerySet:
        """
        Метод для фильтрации товаров по максимальной цене

        @param products: QuerySet с товарами для фильтрации
        @param max_price: максимальное значение цены
        @return: QuerySet с отфильтрованными товарами
        """
        logger.debug(f'Фильтрация по максимальной цене {max_price}')

        filtered_products = products.filter(price__lte=max_price)
        logger.debug(f'Найдено товаров: {len(filtered_products)}')

        return filtered_products

    @classmethod
    def by_title(cls, products: QuerySet, title: str) -> QuerySet:
        """
        Метод для фильтрации товаров по названию

        @param products: QuerySet с товарами для фильтрации
        @param title: название товара для фильтрации
        @return: QuerySet с отфильтрованными товарами
        """
        logger.debug(f'Фильтрация по названию: {title}')

        filtered_products = products.filter(name__icontains=f'{title}')
        logger.debug(f'Найдено товаров: {len(filtered_products)}')

        return filtered_products

    @classmethod
    def by_in_stock(cls, products: QuerySet) -> QuerySet:
        """
        Метод для фильтрации товаров по наличию товара

        @param products: QuerySet с товарами для фильтрации
        @return: QuerySet с отфильтрованными товарами
        """
        logger.debug('Фильтрация по наличию')

        filtered_products = products.filter(count__gt=0)
        logger.debug(f'Найдено товаров: {len(filtered_products)}')

        return filtered_products

    @classmethod
    def by_free_shipping(cls, products: QuerySet) -> QuerySet:
        """
        Метод для фильтрации товаров по возможности бесплатной доставки (цена товара > установленного минимума)

        @param products: QuerySet с товарами для фильтрации
        @return: QuerySet с отфильтрованными товарами
        """
        logger.debug('Фильтрация по бесплатной доставке')

        filtered_products = products.filter(price__gt=config.min_order_cost)
        logger.debug(f'Найдено товаров: {len(filtered_products)}')

        return filtered_products
