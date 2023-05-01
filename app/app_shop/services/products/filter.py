import logging

from typing import Union, Dict
from django.contrib.sessions.models import Session

from ...models import Product, CategoryProduct, ProductTags
from config.admin import config
from ...utils.categories import GetCategory
from ...utils.tags import GetTag


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
    def output_by_tag(cls, tag_name: Union[str, bool]) -> Union[Product, bool]:
        """
        Вывод товаров по определенному тегу
        """

        if not tag_name:
            logger.warning('Тег не передан')
            return False

        else:
            tag_id = GetTag.get_tag_id(tag_name)

            if tag_id:
                products = Product.objects.filter(tags=tag_id, deleted=False)
                logger.debug(f'Возврат товаров по тегу: {tag_name}')
                return products


    @classmethod
    def output_by_filter(cls, session: Session) -> Product:
        """
        Возврат отфильтрованных товаров
        """
        logger.debug(f'Вывод отфильтрованных товаров')

        filters = session.get('filters', False)

        if not filters:
            logger.error('Параметры фильтрации не найдены')
            # TODO Подумать, что делать!!!

        # price_range = filter_parameters['price_range']
        min_price = filters.get('min_price', False)
        max_price = filters.get('max_price', False)
        title = filters.get('title', False)
        in_stock = filters.get('in_stock', False)
        free_shipping = filters.get('free_shipping', False)

        logger.debug(f'Параметры фильтрации: {filters}')

        # FIXME Записывать в сессию id категории, чтобы не делать лишний запрос к БД
        # category = CategoryProduct.objects.get(slug=category_name)

        category_name = session.get('last_category', False)
        tag_name = session.get('last_tag', False)

        if category_name:
            logger.debug(f'Категория извлечена: {category_name}')
            products = cls.output_by_category(category_name=category_name)

        elif tag_name:
            logger.debug(f'Тег извлечен: {tag_name}')
            products = cls.output_by_tag(tag_name=tag_name)

        else:
            products = Product.objects.all()

        if min_price:
            logger.debug('Фильтрация по минимальной цене')
            products = products.filter(price__gte=min_price)
            # logger.debug(f'Найдено товаров: {len(products)}')

        if max_price:
            logger.debug('Фильтрация по максимальной цене')
            products = products.filter(price__lte=max_price)
            # logger.debug(f'Найдено товаров: {len(products)}')

        if title:
            logger.debug('Фильтрация по названию')
            products = products.filter(name__icontains=f'{title}')
            # logger.debug(f'Найдено товаров: {len(products)}')

        if in_stock:
            logger.debug('Фильтрация по наличию')
            products = products.filter(count__gt=0)
            # logger.debug(f'Найдено товаров: {len(products)}')

        if free_shipping:
            logger.debug('Фильтрация по бесплатной доставке')
            products = products.filter(price__gt=config.min_order_cost)
            # logger.debug(f'Найдено товаров: {len(products)}')

        return products
