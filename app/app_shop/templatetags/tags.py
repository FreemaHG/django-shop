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
