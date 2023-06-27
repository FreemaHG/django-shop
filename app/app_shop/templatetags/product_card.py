import logging

from django import template

from ..models.products import ProductImages, Product


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def product_image(product_id: int) -> ProductImages:
    """
    Функция возвращает изображение по id переданного товара

    @param product_id: id товара
    @return: объект изображения
    """
    image = ProductImages.objects.filter(product=product_id).first()

    if not image:
        logger.warning("Изображение не найдено")

    return image
