import logging

from typing import Union
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404

from ...models import Product, CategoryProduct
from ...utils.categories import GetCategory


logger = logging.getLogger(__name__)

class ProductsList:
    """
    Сервис с бизнес-логикой по выводу отфильтрованных товаров
    """

    @classmethod
    def output_by_category(cls, category_name: str) -> Union[Product, bool]:
        """
        Вывод товаров определенной категории
        """
        category_id = GetCategory.get_category_id(category_name)

        if category_id:
            # TODO проверить вывод только активных товаров!
            products = Product.objects.filter(category=category_id, deleted=False)
            logger.info('Товары найдены')
            return products

        else:
            logger.warning('Товары НЕ найдены')
            return False

    @classmethod
    def output_by_tag(cls):
        """ Вывод товаров по определенному тегу """
        ...

    @classmethod
    def output_by_filter(cls):
        """ Вывод отфильтрованных товаров """
        ...
