import logging

from ..services.products.filter import ProductFilter
from ..services.products.sorting import ProductSorted
from ..models import Product, CategoryProduct, ProductTags
from .products_list import ProductsListView
from ..services.session import (
    ProductCategoryTracking,
    ProductTagTracking,
    FilterParametersTracking,
    SortProductsTracing,
    SortProductsTracingForPrice,
)


logger = logging.getLogger(__name__)


class ProductsSortedByPrice(ProductsListView):
    """
    Вывод товаров отсортированных по цене
    """

    def get_queryset(self, **kwargs):
        logger.debug('Вывод товаров, отсортированных ПО ЦЕНЕ')
        session = self.request.session

        # Проверка параметров сортировки по цене
        SortProductsTracing.check_or_create(session=session)
        sorted_data = SortProductsTracingForPrice.check(session=session)

        # Вывод отфильтрованных товаров, если были заданы параметры фильтрации
        filtered_products = ProductFilter.output_by_filter(session=session)

        if sorted_data:
            # Сортировка товаров по цене по возрастанию
            sorted_products = ProductSorted.by_price_up(products=filtered_products)

            logger.info('Сбрасываем параметр сортировки')
            SortProductsTracing.delete(session=session)

        else:
            # Сортировка товаров по цене по убыванию
            sorted_products = ProductSorted.by_price_down(products=filtered_products)

            # Устанавливаем сортировку на "по возрастанию"
            SortProductsTracingForPrice.add_price_up(session=session)

        # ОЧИСТКА всех параметров сортировки, КРОМЕ ЦЕНЫ
        # SortProductsTracing.clear_data(session=session, control_parameter='by_price')

        return sorted_products

    def get_context_data(self, **kwargs):
        """
        Передача индикатора сортировки в шаблон
        """
        session = self.request.session
        context = super().get_context_data(**kwargs)
        sorted_data = SortProductsTracingForPrice.check(session=session)

        if sorted_data:
            context['sorting_indicator_by_price'] = 'Sort-sortBy_dec'  # Сортировка вверх
        else:
            context['sorting_indicator_by_price'] = 'Sort-sortBy_inc'  # Сортировка вниз

        context['filter_parameters'] = FilterParametersTracking.get(session=session)

        return context