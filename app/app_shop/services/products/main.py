import logging

from typing import Dict, List
from django.db.models import Min

from ...models import Product, CategoryProduct

class ProductsForMainService:
    """
    Сервис по выводу товаров для главной страницы
    """
    @classmethod
    def selected_categories(cls) -> List[CategoryProduct]:
        """
        Возврат 3-ех избранных категорий товаров, указанных в настройках сайта
        """
        categories = CategoryProduct.objects.filter(selected=True).annotate(min_price=Min('product__price'))[:3]

        return categories

    # FIXME Добавить после реализации механики покупки товаров
    @classmethod
    def popular_products(cls):
        """
        Возврат популярных продуктов (ТОП по продажам)
        """
        ...

    @classmethod
    def limited_edition(cls) -> List[Product]:
        """
        Возврат товаров с ограниченным тиражом
        """
        products = Product.objects.filter(limited_edition=True)

        return products
