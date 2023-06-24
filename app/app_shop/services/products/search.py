import logging

from django.db.models import Q, QuerySet
from django.http import HttpRequest

from ...models.products import Product


logger = logging.getLogger(__name__)


class ProductsListSearchService:
    """
    Сервис для поиска товаров по названию
    """

    @classmethod
    def search(cls, request: HttpRequest) -> QuerySet:
        """
        Поиск товаров по переданной в URL фразе: частичное / полное совпадение с названием товара,
        совпадение в начале / в конце наименования товара

        @param request: http-запрос с URL вида /search/?query=смартфон
        @return: QuerySet с товарами
        """

        query = request.GET['query']
        logger.debug(f'Поиск товаров по фразе: {query}')

        products = Product.objects.filter(
            Q(name__icontains=query) | Q(name__contains=query) | Q(name__startswith=query) | Q(name__endswith=query) |
            Q(name__icontains=query.capitalize()) | Q(name__contains=query.capitalize()) |
            Q(name__startswith=query.capitalize()) | Q(name__endswith=query.capitalize())
        )

        return products
