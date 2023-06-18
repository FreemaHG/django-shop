import logging

from typing import Dict, List, Union

from django.core.exceptions import ObjectDoesNotExist

from ...models import Product, CategoryProduct
from ...services.products.products_list.filter import ProductFilter
from ...services.products.products_list.sorting import ProductSort


logger = logging.getLogger(__name__)


class ProductsListService:
    """
    Сервис по выводу товаров определенной категории, тегу либо всех.
    Фильтрация и сортировка товаров по входящим параметрам.
    """

    @classmethod
    def output(cls, filter_parameters: Dict):
        logger.debug('Запуск сервиса по выводу товаров')

        group = filter_parameters.get('group', False)
        name = filter_parameters.get('name', False)
        # sort = filter_parameters.get('sort', False)

        # Фильтрация по категории / тегу
        if group == 'category':
            logger.debug(f'Вывод товаров категории: {name}')
            products = cls.output_by_category(category_name=name)

        elif group == 'tag':
            logger.debug(f'Вывод товаров по тегу: {name}')
            products = cls.output_by_tag(tag_name=name)

        else:
            logger.debug('Возврат всех товаров')
            products = Product.objects.all()

        return products


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
