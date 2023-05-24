import logging

from django import template

from ..models import ProductImages, Product


logger = logging.getLogger(__name__)
register = template.Library()

# Не используется!!!
@register.simple_tag
def product_image(product_id: int) -> ProductImages:
    """
    Возвращает изображение по id переданного товара
    """
    image = ProductImages.objects.filter(product=product_id).first()

    if not image:
        logger.warning('Изображение не найдено')

    return image