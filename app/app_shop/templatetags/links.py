import logging

from django import template


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def clear_link_for_sort(link: str) -> str:
    """
    Очистка входящей строки от текста после ключевой фразы 'sort'.
    Добавление спец.символа в конце для корректного парсинга параметров из URL.

    @param link: строка-ссылка
    @return: очищенная строка
    """
    logger.debug(f"Очистка ссылки для сортировки: {link}")

    if "&sort" in link:
        link = link.split("&sort")[0]

    elif "?sort" in link:
        link = link.split("?sort")[0]

    elif "&page=" in link:
        link = link.split("&page=")[0]

    elif "?page=" in link:
        link = link.split("?page=")[0]

    if "?" not in link:
        link += "?"
    else:
        link += "&"

    logger.info(f"Возврат очищенной ссылки: {link}")

    return link


@register.simple_tag
def clear_link_for_paginate(link: str) -> str:
    """
    Очистка входящей строки от текста после ключевой фразы 'page'.
    Добавление спец.символа в конце для корректного парсинга параметров из URL.

    @param link: строка-ссылка
    @return: очищенная строка
    """
    logger.warning(f"Очистка ссылки для пагинации: {link}")

    if "&page=" in link:
        link = link.split("&page=")[0]

    elif "?page=" in link:
        link = link.split("?page=")[0]

    if "?" not in link:
        link += "?"
    else:
        link += "&"

    logger.info(f"Возврат очищенной ссылки: {link}")

    return link


@register.simple_tag
def clear_link_for_next(link: str) -> str:
    """
    Очистка входящей строки от текста ДО ключевой фразы '?next'

    @param link: строка-ссылка
    @return: очищенная строка
    """
    logger.debug(f'Очистка ссылки от "?next": {link}')

    if "?next" in link:
        link = link.split("?next=")[-1]

    logger.info(f"Возврат очищенной ссылки: {link}")

    return link
