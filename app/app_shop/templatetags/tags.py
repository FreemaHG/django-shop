import logging

from typing import Union
from django import template
from django.db.models import QuerySet

from ..models.products import ProductTags, Product


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def output_tags():
    """
    Вывод всех тегов
    """
    tags = ProductTags.objects.all()
    return tags


@register.simple_tag
def tags_for_product(product: Product) -> QuerySet:
    """
    Вывод всех активных тегов товара

    @param product: объект товара
    @return: QuerySet с активными тегами
    """
    logger.debug(f'Возврат активных тегов товара: {product.name}')

    tags = product.tags.filter(deleted=False)
    logger.debug(f'Найдено тегов: {tags.count()}')

    return tags


@register.simple_tag
def check_for_word_end(number: int = None) -> Union[str, None]:
    """
    Проверка входящего числа для вывода корректного окончания слова в шаблоне
    для обозначения кол-ва комментариев к товару

    @param number: число - кол-во товара
    @return: строка - окончание слова
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
