import logging

from django import template
from django.http import HttpRequest

from ..models.products import CategoryProduct, Product
from ..services.shop_cart.logic import CartProductsListService, ProductsCartUserService
# from ..utils.models.check import check_active_products


logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag()
def output_categories():
    """
    Возвращаем активные родительские категории товаров, в которых есть активные товары
    """
    # FIXME: Добавить проверку на наличие активных товаров в категории (после добавления товаров)!!!
    return CategoryProduct.objects.filter(deleted=False, parent=None).order_by('id')


@register.simple_tag(takes_context=True)
def products_cart(context):
    """
    Возвращает кол-во товаров в корзине текущего пользователя
    """
    logger.debug('Вывод в header кол-ва и стоимости товаров в корзине пользователя')
    records_number = 0
    total_cost = 0

    # FIXME Кэшировать данные
    records = CartProductsListService.output(context['request'])

    if records:
        for record in records:
            records_number += record.count

        total_cost = ProductsCartUserService.total_cost(records)

    logger.debug(f'Товаров: {records_number}, стоимость: {total_cost} руб')

    return records_number, total_cost
