import logging

from typing import Union, Dict
from django.contrib.sessions.models import Session

from ...models import Product, CategoryProduct
from config.admin import config
from ...utils.categories import GetCategory


logger = logging.getLogger(__name__)

class ProductFilter:
    """
    Сервис с бизнес-логикой по выводу отфильтрованных товаров
    """

    @classmethod
    def output_by_category(cls, category_name: Union[str, bool]) -> Union[Product, bool]:
        """
        Вывод товаров определенной категории
        """
        logger.warning(f'Вывод товаров категории: {category_name}')

        if not category_name or category_name == 'all':
            logger.debug('Возврат ВСЕХ товаров')
            return Product.objects.all()

        else:
            category_id = GetCategory.get_category_id(category_name)

            if category_id:
                products = Product.objects.filter(category=category_id, deleted=False)
                logger.debug(f'Возврат товаров категории: {category_name}')
                return products


    @classmethod
    def output_by_tag(cls):
        """ Вывод товаров по определенному тегу """
        ...

    @classmethod
    def output_by_filter(cls, filter_parameters: Dict, session: Session) -> Product:
        """
        Возврат отфильтрованных товаров
        """
        logger.debug(f'Вывод отфильтрованных товаров')

        # price_range = filter_parameters['price_range']
        min_price = filter_parameters['min_price']
        max_price = filter_parameters['max_price']
        title = filter_parameters['title']
        in_stock = filter_parameters['in_stock']
        free_shipping = filter_parameters['free_shipping']

        category_name = session.get('last_category', False)
        logger.debug(f'Категория извлечена: {category_name}')

        # FIXME Записывать в сессию id категории, чтобы не делать лишний запрос к БД
        # category = CategoryProduct.objects.get(slug=category_name)

        products = cls.output_by_category(category_name)

        if min_price:
            logger.debug('Фильтрация по минимальной цене')
            products = products.filter(price__gte=min_price)
            logger.debug(f'Найдено товаров: {len(products)}')

        if max_price:
            logger.debug('Фильтрация по максимальной цене')
            products = products.filter(price__lte=max_price)
            logger.debug(f'Найдено товаров: {len(products)}')

        if title:
            logger.debug('Фильтрация по названию')
            products = products.filter(name__icontains=f'{title}')
            logger.debug(f'Найдено товаров: {len(products)}')

        if in_stock:
            logger.debug('Фильтрация по наличию')
            products = products.filter(count__gt=0)
            logger.debug(f'Найдено товаров: {len(products)}')

        if free_shipping:
            logger.debug('Фильтрация по бесплатной доставке')
            products = products.filter(price__gt=config.min_order_cost)
            logger.debug(f'config.min_order_cost: {config.min_order_cost}')
            logger.debug(f'Найдено товаров: {len(products)}')

        return products
