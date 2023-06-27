import logging

from typing import Dict, Tuple
from django import template
from django.core.cache import cache
from django.db.models import QuerySet

# from config.admin import config
from config.utils.configuration import get_config
from ..models.products import CategoryProduct
from ..services.shop_cart.logic import CartProductsListService, ProductsCartUserService


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag()
def output_categories() -> QuerySet:
    """
    Функция возвращает активные родительские категории товаров, в которых есть активные товары

    @return: QuerySet с категориями товаров
    """
    config = get_config()

    categories = cache.get_or_set(
        "categories",
        CategoryProduct.objects.filter(deleted=False, parent=None).order_by("id"),
        60 * config.caching_time,
    )

    return categories


@register.simple_tag(takes_context=True)
def products_cart(context: Dict) -> Tuple[int, int]:
    """
    Функция возвращает кол-во товаров в корзине текущего пользователя и их общую стоимость

    @param context: словарь - контекстная переменная
    @return: кол-во записей, общая стоимость товаров
    """
    logger.debug("Вывод в header кол-ва и стоимости товаров в корзине пользователя")

    records_number = 0
    total_cost = 0

    records = CartProductsListService.all_products(context["request"])

    if records:
        for record in records:
            records_number += record.count

        total_cost = ProductsCartUserService.total_cost(records)

    logger.debug(f"Товаров: {records_number}, стоимость: {total_cost} руб")

    return records_number, total_cost
