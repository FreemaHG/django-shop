import logging

from typing import Dict, List

from django.db.models import Q

from ...models import Product
from ...services.products.products_list.filter import ProductFilter
from ...services.products.products_list.sorting import ProductSort


logger = logging.getLogger(__name__)


class ProductsListSearchService:
    """
    Поиск товаров
    """
    @classmethod
    def search(cls, query: str) -> List[Product]:
        """
        Поиск товаров по названию по переданной фразе: частичное / полное совпадение с названием товара,
        совпадение в начале / в конце названия товара
        """
        logger.debug(f'Поиск товаров по фразе: {query}')
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(name__contains=query) | Q(name__startswith=query) | Q(name__endswith=query) |
            Q(name__icontains=query.capitalize()) | Q(name__contains=query.capitalize()) |
            Q(name__startswith=query.capitalize()) | Q(name__endswith=query.capitalize())
        )

        return products
