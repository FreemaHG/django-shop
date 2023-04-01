from django import template

from ..models import CategoryProduct
from ..utils.models.check import check_active_products


register = template.Library()

@register.simple_tag()
def output_categories():
    """ Возвращаем активные родительские категории товаров, в которых есть активные товары """

    # FIXME: Добавить проверку на наличие активных товаров в категории!!!
    return CategoryProduct.objects.filter(deleted=False, parent=None).order_by('id')
