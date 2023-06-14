import logging

from django.db.models import QuerySet, Count


logger = logging.getLogger(__name__)


class ProductSort:
    """
    Сервис с бизнес-логикой по сортировке товаров по популярности, цене, отзывам и новизне
    """

    @classmethod
    def by_popularity_up(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по популярности (кол-ву покупок) (по возрастанию)
        """
        logger.debug('Сортировка по популярности (кол-ву продаж): по возрастанию')
        sorted_products = products.order_by('purchases')
        return sorted_products

    @classmethod
    def by_popularity_down(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по популярности (кол-ву покупок) (по убыванию)
        """
        logger.debug('Сортировка по популярности (кол-ву продаж): по убыванию')
        sorted_products = products.order_by('-purchases')
        return sorted_products

    @classmethod
    def by_price_up(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по цене (по возрастанию)
        """
        logger.debug('Сортировка по цене: по возрастанию')
        sorted_products = products.order_by('price')
        return sorted_products

    @classmethod
    def by_price_down(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по цене (по убыванию)
        """
        logger.debug('Сортировка по цене: по убыванию')
        sorted_products = products.order_by('-price')
        return sorted_products

    @classmethod
    def by_reviews_up(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по отзывам (их кол-ву) (по возрастанию)
        """
        logger.debug('Сортировка по отзывам: по возрастанию')
        sorted_products = products.annotate(count_comments=Count('productreviews')).order_by('-count_comments')
        return sorted_products

    @classmethod
    def by_reviews_down(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по отзывам (их кол-ву) (по убыванию)
        """
        logger.debug('Сортировка по отзывам: по убыванию')
        sorted_products = products.annotate(count_comments=Count('productreviews')).order_by('count_comments')
        return sorted_products

    @classmethod
    def by_novelty_up(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по новизне (дате публикации товара) (по возрастанию)
        """
        logger.debug('Сортировка по новизне: по возрастанию')
        sorted_products = products.order_by('created_at')
        return sorted_products

    @classmethod
    def by_novelty_down(cls, products: QuerySet) -> QuerySet:
        """
        Сортировка товаров по новизне (дате публикации товара) (по убыванию)
        """
        logger.debug('Сортировка по новизне: по убыванию')
        sorted_products = products.order_by('-created_at')
        return sorted_products
