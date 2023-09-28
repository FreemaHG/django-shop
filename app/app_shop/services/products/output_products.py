import logging

from typing import Dict, List, Union
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from app.app_shop.models.products import Product, CategoryProduct


logger = logging.getLogger(__name__)


class ProductsListService:
    """
    Сервис по выводу товаров определенной категории, тегу либо всех.
    Фильтрация и сортировка товаров по входящим параметрам.
    """

    @classmethod
    def output(cls, filter_parameters: Dict) -> QuerySet:
        """
        Метод для вывода товаров, отфильтрованных и отсортированных по переданным параметрам

        @param filter_parameters: словарь с параметрами фильтрации и сортировки
        @return: QuerySet c отфильтрованными / отсортированными товарами
        """
        logger.debug("Запуск сервиса по выводу товаров")

        group = filter_parameters.get("group", False)
        name = filter_parameters.get("name", False)

        # Фильтрация по категории / тегу
        if group == "category" and name is not False:
            logger.debug(f"Вывод товаров категории: {name}")
            return cls.output_by_category(category_name=name)

        elif group == "tag" and name is not False:
            logger.debug(f"Вывод товаров по тегу: {name}")
            return cls.output_by_tag(tag_name=name)

        elif group is not False and name is False:
            logger.error("Не передано наименование категории или тега для фильтрации")

        else:
            logger.debug("Возврат всех товаров")

        return Product.objects.all()

    @classmethod
    def output_by_category(cls, category_name: str) -> Union[QuerySet, List]:
        """
        Метод для вывода товаров определенной категории

        @param category_name: название категории
        @return: QuerySet с товарами категории / пустой список
        """
        logger.debug(f"Возврат товаров категории: {category_name}")

        try:
            category = CategoryProduct.objects.get(slug=category_name)
            logger.debug(f"Категория найдена: {category.title}")

        except ObjectDoesNotExist:
            logger.warning("Категория не найдена")
            return []

        sub_categories = category.get_descendants(
            include_self=True
        )  # Дочерние категории
        products = (
            Product.objects.select_related("category")
            .prefetch_related("images")
            .filter(category__in=sub_categories, deleted=False)
        )

        logger.debug(f"Найдено товаров: {products.count()}")

        return products

    @classmethod
    def output_by_tag(cls, tag_name: str) -> QuerySet:
        """
        Метод для вывода товаров по определенному тегу

        @param tag_name: наименование тега
        @return: QuerySet с товарами
        """
        logger.debug(f"Возврат товаров по тегу: {tag_name}")

        products = Product.objects.prefetch_related("tags", "images").filter(
            tags__slug=tag_name, deleted=False
        )
        logger.debug(f"Найдено товаров: {products.count()}")

        return products
