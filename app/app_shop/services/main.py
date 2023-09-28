import random
import logging

from typing import Dict
from django.db.models import Min, QuerySet
from django.http import HttpRequest
from django.core.cache import cache

from app.app_shop.services.shop_cart.logic import CartProductsListService
from app.app_shop.models.products import Product, CategoryProduct


logger = logging.getLogger(__name__)


class ProductsForMainService:
    """
    Сервис по выводу товаров и категорий на главной странице
    """

    _CACHING_TIME = 60 * 60 * 24  # 1 день

    @classmethod
    def save_data(cls, context: Dict, request: HttpRequest) -> Dict:
        """
        Метод для сохранения данных в переменную контекста для последующего вывода в шаблоне главной страницы

        @param context: словарь
        @param request: объект http-запроса
        @return: словарь с данными по товарам и категориям
        """

        context["selected_categories"] = ProductsForMainService.selected_categories()
        context["limited_products"] = ProductsForMainService.limited_edition()
        context["popular_products"] = ProductsForMainService.popular_products()

        # id товаров в корзине текущего пользователя
        # для корректного отображения кнопки добавления/удаления товара из корзины в карточке товара
        context["products_id"] = CartProductsListService.id_products(request=request)

        return context

    @classmethod
    def selected_categories(cls) -> QuerySet:
        """
        Метод для возврата 3-ех избранных категорий товаров, указанных в конфигурации сайта

        @return: QuerySet с избранными категориями
        """

        categories = cache.get_or_set(
            "selected_categories",
            CategoryProduct.objects.only("title", "slug", "image")
            .filter(selected=True)
            .annotate(min_price=Min("product__price"))[:3],
            cls._CACHING_TIME,
        )

        return categories

    @classmethod
    def popular_products(cls) -> QuerySet:
        """
        Метод возвращает ТОП 8 популярных продуктов (ТОП по продажам).
        Сначала отбирается 30 наиболее популярных товаров, из которых случайным образом возвращается 8

        @return: QuerySet с товарами
        """

        most_popular_products = cache.get_or_set(
            "popular_products",
            list(
                Product.objects.select_related("category")
                .only("id", "name", "category__title", "price", "discount")
                .order_by("-purchases")[:30]
            ),
            cls._CACHING_TIME,
        )

        random.shuffle(most_popular_products)

        return most_popular_products[:8]

    @classmethod
    def limited_edition(cls) -> QuerySet:
        """
        Метод возвращает товары, помеченные 'ограниченным тиражом'

        @return: QuerySet с товарами
        """
        products = cache.get_or_set(
            "limited_edition",
            Product.objects.select_related("category")
            .only("id", "name", "category__title", "price", "discount")
            .filter(limited_edition=True),
            cls._CACHING_TIME,
        )

        return products
