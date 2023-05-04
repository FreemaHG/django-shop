import logging

from django import template

from ..models import ProductTags


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
def clear_link(link: str) -> str:
    """
    Очистка входящей строки от текста после ключевой фразы 'sort'.
    Добавление спец.символа в конце для корректного парсинга параметров из URL.
    """
    if '&sort' in link:
        link = link.split('&sort')[0]

    elif '?sort' in link:
        link = link.split('?sort')[0]

    logger.debug(f'Возврат очищенной ссылки: {link}')

    if '?' not in link:
        link += '?'
    else:
        link += '&'

    return link
