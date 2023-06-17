import logging

from typing import List
from django.http import HttpRequest

from ...models import ProductBrowsingHistory, Product


logger = logging.getLogger(__name__)


class ProductBrowsingHistoryService:
    """
    Сервис для сохранения и вывода истории просмотренных товаров пользователем
    """

    @classmethod
    def history_products(cls, request: HttpRequest) -> List[ProductBrowsingHistory]:
        """
        Метод для вывода истории просмотренных товаров

        @param request: http-запрос
        @return: список с отфильтрованными записями по текущему пользователю из запроса
        """

        logger.debug('Вывод истории просмотров товаров')
        records = ProductBrowsingHistory.objects.filter(user=request.user)

        return records

    @classmethod
    def save_view(cls, request: HttpRequest, product: Product) -> None:
        """
        Метод для сохранения записи о просмотренном товаре

        @param request: http-запрос
        @param product: объект товара
        @return: None
        """

        logger.debug('Сохранение записи о просмотренном товаре')

        # Выполняем проверку, сравнивая id текущего товара с id последних 8-ми сохраненных товаров в истории текущего
        # пользователя, чтобы не дублировать записи в истории просмотра
        last_records = ProductBrowsingHistory.objects.filter(user=request.user).values_list('product', flat=True)[:8]

        if not product.id in last_records:
            ProductBrowsingHistory.objects.create(
                user=request.user,
                product=product
            )
            logger.info('Внесена запись о просмотре товара')

        else:
            logger.warning('Товар уже есть среди последних записей пользователя')
