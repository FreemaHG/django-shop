import logging

from typing import Dict

from ...models import Product
from ...services.products.products_list.filter import ProductFilter
from ...services.products.products_list.sorting import ProductSort


logger = logging.getLogger(__name__)


class ProductsListService:
    """
    Сервис по выводу товаров определенной категории, тегу либо всех.
    Фильтрация и сортировка товаров по входящим параметрам.
    """
    @classmethod
    def output(cls, filter_parameters: Dict):
        logger.debug('Запуск сервиса по выводу товаров')

        group = filter_parameters.get('group', False)
        name = filter_parameters.get('name', False)
        sort = filter_parameters.get('sort', False)

        # Фильтрация по категории / тегу
        if group == 'category':
            logger.debug(f'Вывод товаров категории: {name}')
            products = ProductFilter.output_by_category(category_name=name)

        elif group == 'tag':
            logger.debug(f'Вывод товаров по тегу: {name}')
            products = ProductFilter.output_by_tag(tag_name=name)

        else:
            logger.debug('Возврат всех товаров')
            products = Product.objects.all()

        # Фильтрация по переданным параметрам
        products = ProductFilter.output_by_filter(products=products, filters=filter_parameters)

        # Сортировка
        if sort:
            if sort == 'by_price_down':
                products = ProductSort.by_price_down(products=products)

            elif sort == 'by_price_up':
                products = ProductSort.by_price_up(products=products)

            elif sort == 'by_novelty_down':
                products = ProductSort.by_novelty_down(products=products)

            elif sort == 'by_novelty_up':
                products = ProductSort.by_novelty_up(products=products)

        else:
            logger.warning('Параметр сортировки не задан')

        return products