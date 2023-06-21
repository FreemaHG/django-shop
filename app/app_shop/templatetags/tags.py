import logging

from typing import List, Union
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
def check_for_word_end(number: int = None) -> Union[str, None]:
    """
    Проверка входящего числа для вывода корректного окончания слова в шаблоне
    для обозначения кол-ва комментариев к товару
    """
    logger.debug(f'Проверка входящего числа: {number}')

    if number:
        if str(number)[-1] in ['5', '6', '7', '8', '9', '0'] or str(number)[-2:] in ['11', '12', '13', '14']:
            return 'ов'

        elif str(number)[-1] in ['2', '3', '4']:
            return 'а'

        else:
            return ''

    else:
        logger.warning('Не передан числовой аргумент')
