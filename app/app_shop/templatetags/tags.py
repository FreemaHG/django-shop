import logging

from typing import List
from django import template
from django.http import HttpRequest

from ..models import ProductTags, Product


logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def output_tags():
    """
    Вывод всех тегов
    """
    # FIXME Переделать на вывод популярных тегов для выводимых товаров
    tags = ProductTags.objects.all()

    return tags


@register.simple_tag
def tags_for_product(product: Product) -> List[ProductTags]:
    """
    Вывод всех активных тегов товара
    """
    logger.debug(f'Возврат активных тегов товара: {product.name}')
    tags = product.tags.filter(deleted=False)

    logger.debug(f'Найдено тегов: {len(tags)}')
    return tags


@register.simple_tag
def check_for_word_end(number: int) -> str:
    """
    Проверка входящего числа для вывода корректного окончания в шаблоне
    """
    logger.debug(f'Проверка входного числа: {number}')

    if str(number)[-1] in ['5', '6', '7', '8', '9', '0'] or str(number)[-2:] in ['11', '12', '13', '14']:
        # logger.debug('Возврат окончания: "ов"')
        return 'ов'

    elif str(number)[-1] in ['2', '3', '4']:
        # logger.debug('Возврат окончания: "а"')
        return 'а'

    else:
        # logger.debug('Нет окончания')
        return ''


# @register.simple_tag
# def delivery_cost(request: HttpRequest):
#     """
#     Возврат нужного urlpatternв для формы зависимости от того, авторизован пользователь или нет
#     """
#     logger.debug(f'Определение ссылки для формы')
#
#     if request.user.is_authenticated:
#         logger.debug('Пользователь авторизован. Возврат ссылки для регистрации заказа')
#         return 'shop:order_registration', ''
#     else:
#         current_url = request.path
#         logger.debug(f'Пользователь не авторизован. Возврат ссылки для авторизации с перенаправлением на: {current_url}')
#         # return f'user:registration?next={current_url}'
#         return 'user:registration', f'{current_url}'
