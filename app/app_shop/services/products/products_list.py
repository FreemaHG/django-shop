import logging

from typing import Union, Dict

from ...models import Product
from config.admin import config
from ...utils.categories import GetCategory


logger = logging.getLogger(__name__)

class ProductsList:
    """
    Сервис с бизнес-логикой по выводу отфильтрованных товаров
    """

    @classmethod
    def output_by_category(cls, category_name: str) -> Union[Product, bool]:
        """
        Вывод товаров определенной категории
        """
        category_id = GetCategory.get_category_id(category_name)

        if category_id:
            products = Product.objects.filter(category=category_id, deleted=False)
            logger.info(f'Категория: {category_name}. Товары найдены')
            return products
        else:
            logger.warning(f'Категория: {category_name}. Товары НЕ найдены')
            return False


    @classmethod
    def output_by_tag(cls):
        """ Вывод товаров по определенному тегу """
        ...

    @classmethod
    def output_by_filter(cls, context_data: Dict) -> Product:
        """
        Возврат отфильтрованных товаров
        """
        logger.debug('Запуск метода output_by_filter')
        logger.debug(f'context_data: {context_data}')

        price = context_data.get('price', False)
        title = context_data.get('title', False)
        in_stock = context_data.get('in_stock', False)
        free_shipping = context_data.get('free_shipping', False)

        # FIXME заменить на передаваемые в запросе товары
        products = Product.objects.all()

        if price:
            logger.debug('Сортировка по цене')
            price_range = price.split(';')
            start_price, end_price = price_range[0], price_range[1]
            products = products.filter(price__range=(start_price, end_price))

        if title:
            logger.debug('Сортировка по названию')
            products = products.filter(name__icontains=f'{title}')

        if in_stock:
            logger.debug('Сортировка по наличию')
            products = products.filter(count__gt=0)

        if free_shipping:
            logger.debug('Сортировка по бесплатной доставке')
            products = products.filter(price__gt=config.min_order_cost)

        return products
