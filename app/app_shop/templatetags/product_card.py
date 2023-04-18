import logging

from django import template

from ..models import ProductImages, Product


logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def product_image(product_id: int) -> ProductImages:
    """
    Возвращает изображение по id переданного товара
    """
    image = ProductImages.objects.filter(product=product_id).first()
    logger.info('Изображение найдено')

    return image
