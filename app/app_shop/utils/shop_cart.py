from typing import List
import logging
from django.http import HttpRequest

from ..services.shop_cart.logic import CartProductsListService


logger = logging.getLogger(__name__)

def get_id_products_in_cart(request: HttpRequest) -> List[int]:
    """
    Получаем список с id товаров в корзине текущего пользователя
    """
    id_list = []

    logger.debug('Получение списка id товаров в корзине текущего пользователя')
    products = CartProductsListService.output(request=request)

    # FIXME Сделать умнее!
    for record in products:
        id_list.append(record.product.id)

    logger.info(f'Список с id товаров: {id_list}')

    return id_list
