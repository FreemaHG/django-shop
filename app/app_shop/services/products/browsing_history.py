import logging

from django.contrib.auth.models import User
from django.http import HttpRequest

from ...models import ProductBrowsingHistory, Product


logger = logging.getLogger(__name__)


class ProductBrowsingHistoryServices:
    """
    Сервис для сохранения истории просмотренных товаров пользователем
    """

    @classmethod
    def history_products(cls, request: HttpRequest):
        """
        История просмотренных товаров
        """
        logger.debug('Вывод истории просмотров товаров')
        records = ProductBrowsingHistory.objects.filter(user=request.user)

        return records

    @classmethod
    def save_view(cls, request: HttpRequest, product: Product):
        """
        Сохранение записи о просмотренном товаре
        """
        # TODO Можно сделать задание по расписанию для удаления старых записей
        logger.debug('Сохранение записи о просмотренном товаре')
        last_records = ProductBrowsingHistory.objects.filter(user=request.user).values_list('product', flat=True)[:8]

        if not product.id in last_records:
            ProductBrowsingHistory.objects.create(
                user=request.user,
                product=product
            )
            logger.info('Внесена запись о просмотре товара')

        else:
            logger.warning('Товар уже есть среди последних записей пользователя')
