import logging

from django.db.models import QuerySet
from django.http import HttpRequest

from ...models.products import ProductBrowsingHistory, Product


logger = logging.getLogger(__name__)


class ProductBrowsingHistoryService:
    """
    Сервис для сохранения и вывода истории просмотренных товаров пользователем
    """

    @classmethod
    def history_products(cls, request: HttpRequest) -> QuerySet:
        """
        Метод для вывода истории просмотренных товаров

        @param request: объект http-запроса
        @return: список с отфильтрованными записями по текущему пользователю из запроса
        """
        logger.debug("Вывод истории просмотров товаров")
        records = ProductBrowsingHistory.objects.select_related(
            "product", "product__category"
        ).filter(user=request.user)

        return records

    @classmethod
    def save_view(cls, request: HttpRequest, product: Product) -> None:
        """
        Метод для сохранения записи о просмотренном товаре

        @param request: объект http-запроса
        @param product: просмотренный товар
        @return: None
        """
        logger.debug("Сохранение записи о просмотренном товаре")

        # Выполняем проверку, сравнивая id текущего товара с id последних 8-ми сохраненных товаров в истории текущего
        # пользователя, чтобы не дублировать записи в истории просмотра
        last_records = ProductBrowsingHistory.objects.filter(
            user=request.user
        ).values_list("product", flat=True)[:8]

        if not product.id in last_records:
            ProductBrowsingHistory.objects.create(user=request.user, product=product)
            logger.info("Внесена запись о просмотре товара")

        else:
            logger.warning("Товар уже есть среди последних записей пользователя")
