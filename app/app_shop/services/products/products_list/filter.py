import logging

from typing import Union, Dict, List
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from config.admin import config
from ....models import Product, CategoryProduct


logger = logging.getLogger(__name__)

class ProductFilter:
    """
    Сервис с бизнес-логикой по выводу отфильтрованных товаров
    """

    @classmethod
    def output_by_category(cls, category_name: Union[str, bool]) -> Union[Product, List]:
        """
        Вывод товаров определенной категории
        """
        try:
            category = CategoryProduct.objects.get(slug=category_name)
            logger.debug(f'Категория найдена: {category.title}')

        except ObjectDoesNotExist:
            logger.warning('Категория не найдена')
            return []

        sub_categories = category.get_descendants(include_self=True)  # Дочерние категории
        products = Product.objects.filter(category__in=sub_categories, deleted=False)
        # products = Product.objects.filter(category__slug=category_name, deleted=False)

        return products


    @classmethod
    def output_by_tag(cls, tag_name: Union[str, bool]) -> Union[Product, bool]:
        """
        Вывод товаров по определенному тегу
        """
        products = Product.objects.filter(tags__slug=tag_name, deleted=False)
        logger.debug(f'Фильтр: возврат товаров по тегу: {tag_name}. Найдено товаров: {len(products)}')

        return products


    @classmethod
    def output_by_filter(cls, products: QuerySet, filters: Dict) -> QuerySet:
        """
        Возврат отфильтрованных товаров
        """

        if filters:
            min_price = filters.get('min_price', False)
            max_price = filters.get('max_price', False)
            title = filters.get('title', False)
            in_stock = filters.get('in_stock', False)
            free_shipping = filters.get('free_shipping', False)

            if min_price:
                logger.debug(f'Фильтрация по минимальной цене: {min_price}')
                products = products.filter(price__gte=min_price)
                # logger.debug(f'Найдено товаров: {len(products)}')

            if max_price:
                logger.debug(f'Фильтрация по максимальной цене {max_price}')
                products = products.filter(price__lte=max_price)
                # logger.debug(f'Найдено товаров: {len(products)}')

            if title:
                logger.debug(f'Фильтрация по названию: {title}')
                products = products.filter(name__icontains=f'{title}')
                # logger.debug(f'Найдено товаров: {len(products)}')

            if in_stock:
                logger.debug('Фильтрация по наличию')
                products = products.filter(count__gt=0)
                # logger.debug(f'Найдено товаров: {len(products)}')

            if free_shipping:
                logger.debug('Фильтрация по бесплатной доставке')
                products = products.filter(price__gt=config.min_order_cost)
                # logger.debug(f'Найдено товаров: {len(products)}')

        else:
            logger.warning('Параметры фильтрации не заданы')

        return products
