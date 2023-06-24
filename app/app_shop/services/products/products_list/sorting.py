import logging
from typing import Dict

from django.db.models import QuerySet, Count


logger = logging.getLogger(__name__)


class ProductSortService:
    """
    Сервис по сортировке товаров по популярности, цене, отзывам и новизне
    """

    @classmethod
    def output(cls, products: QuerySet, filters: Dict) -> QuerySet:
        """
        Метод возвращает отсортированные товары по переданным параметрам
        
        @param products: QuerySet с товарами для сортировки
        @param filters: словарь с параметрами сортировки
        @return: QuerySet с отсортированными товарами
        """
        sort = filters.get('sort', False)

        if sort:
            if sort == 'by_price_down':
                products = cls.by_price_down(products=products)

            elif sort == 'by_price_up':
                products = cls.by_price_up(products=products)

            elif sort == 'by_popularity_down':
                products = cls.by_popularity_down(products=products)

            elif sort == 'by_popularity_up':
                products = cls.by_popularity_up(products=products)

            elif sort == 'by_reviews_down':
                products = cls.by_reviews_down(products=products)

            elif sort == 'by_reviews_up':
                products = cls.by_reviews_up(products=products)

            elif sort == 'by_novelty_down':
                products = cls.by_novelty_down(products=products)

            elif sort == 'by_novelty_up':
                products = cls.by_novelty_up(products=products)
        else:
            logger.warning('Параметр сортировки не задан')

        return products


    @classmethod
    def by_popularity_up(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по популярности (кол-ву покупок) (по возрастанию)
        
        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по популярности (кол-ву продаж): по возрастанию')
        
        sorted_products = products.order_by('purchases')
        return sorted_products


    @classmethod
    def by_popularity_down(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по популярности (кол-ву покупок) (по убыванию)
        
        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по популярности (кол-ву продаж): по убыванию')
        
        sorted_products = products.order_by('-purchases')
        return sorted_products


    @classmethod
    def by_price_up(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по цене (по возрастанию)

        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по цене: по возрастанию')

        sorted_products = products.order_by('price')
        return sorted_products


    @classmethod
    def by_price_down(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по цене (по убыванию)

        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по цене: по убыванию')

        sorted_products = products.order_by('-price')
        return sorted_products


    @classmethod
    def by_reviews_up(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по отзывам (их кол-ву) (по возрастанию)

        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по отзывам: по возрастанию')

        sorted_products = products.annotate(count_comments=Count('productreviews')).order_by('-count_comments')
        return sorted_products


    @classmethod
    def by_reviews_down(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по отзывам (их кол-ву) (по убыванию)

        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по отзывам: по убыванию')

        sorted_products = products.annotate(count_comments=Count('productreviews')).order_by('count_comments')
        return sorted_products


    @classmethod
    def by_novelty_up(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по новизне (дате публикации товара) (по возрастанию)

        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по новизне: по возрастанию')

        sorted_products = products.order_by('created_at')
        return sorted_products


    @classmethod
    def by_novelty_down(cls, products: QuerySet) -> QuerySet:
        """
        Метод для сортировки товаров по новизне (дате публикации товара) (по убыванию)

        @param products: QuerySet с товарами для сортировки
        @return: QuerySet с отсортированными товарами
        """
        logger.debug('Сортировка по новизне: по убыванию')

        sorted_products = products.order_by('-created_at')
        return sorted_products
