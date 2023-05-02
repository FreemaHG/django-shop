import logging

from django.urls import reverse
from django.views.generic import View, ListView
from django.shortcuts import render, redirect

from ..services.products.filter import ProductFilter
from ..models import Product, CategoryProduct, ProductTags
from ..services.session import (
    ProductCategoryTracking,
    ProductTagTracking,
    FilterParametersTracking,
    SortProductsTracing,
    SortProductsTracingForPrice,
)


logger = logging.getLogger(__name__)


class ProductsListView(ListView):
    """
    Вывод каталога товаров (определенной категории или всех)
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self, **kwargs):
        session = self.request.session
        category_name = self.kwargs.get('category_name', False)
        logger.debug(f'Вывод товаров категории: {category_name}')

        # Сброс параметров фильтрации и сортировки товаров
        FilterParametersTracking.delete(session=session)
        SortProductsTracing.delete(session=session)

        # ФИКСИРУЕМ в сессии просматриваемую КАТЕГОРИЮ товаров
        ProductCategoryTracking.add(session=session, category=category_name)

        # УДАЛЯЕМ из сессии данные о последних просматриваемых товарах определенного ТЕГА
        ProductTagTracking.delete(session=session)

        # Товары нужной категории
        products = ProductFilter.output_by_category(category_name=category_name)

        return products


class ProductsForTagLIstView(ProductsListView):
    """
    Вывод товаров определенного тега
    """

    def get_queryset(self, **kwargs):
        session = self.request.session
        tag_name = self.kwargs.get('tag_name', False)
        logger.debug(f'Вывод товаров по тегу: {tag_name}')

        # Сброс параметров фильтрации и сортировки товаров
        FilterParametersTracking.delete(session=session)
        SortProductsTracing.delete(session=session)

        # ФИКСИРУЕМ в сессии просматриваемые товары определенного ТЕГА
        ProductTagTracking.add(session=session, tag=tag_name)

        # УДАЛЯЕМ из сессии данные о последней просматриваемой КАТЕГОРИИ товаров текущего пользователя
        ProductCategoryTracking.delete(session=session)

        # Товары определенного тега
        products = ProductFilter.output_by_tag(tag_name=tag_name)

        return products


class ProductsFilterListView(View):
    """
    Вывод отфильтрованных товаров
    """
    # TODO Сделать пагинацию
    # paginate_by = 8

    def post(self, request):
        session = request.session
        FilterParametersTracking.delete(session=session)  # Очистка старых данных

        logger.debug(f'Фильтр: входные параметры: {request.POST}')

        new_filter_parameters = {
            # 'price_range': request.POST.get('price', False),
            'min_price': request.POST.get('min_price', False),
            'max_price': request.POST.get('max_price', False),
            'title': request.POST.get('title', False),
            'in_stock': True if request.POST.get('in_stock', False) else False,
            'free_shipping': True if request.POST.get('free_shipping', False) else False,
        }

        # СОХРАНЕНИЕ параметров фильтрации текущего пользователя
        FilterParametersTracking.add(new_filter_parameters=new_filter_parameters, session=session)

        # Вывод отфильтрованных товаров
        res_products = ProductFilter.output_by_filter(session=session)

        # Вывод параметров фильтрации ТЕКУЩЕГО пользователя
        filter_parameters = FilterParametersTracking.get(session=session)

        return render(request, '../templates/app_shop/catalog.html', {
            'products': res_products,
            'filter_parameters': filter_parameters,
        })


class ResetFiltersView(View):
    """
    Сброс параметров фильтрации
    """
    # TODO Сделать пагинацию
    # paginate_by = 8

    def get(self, request):
        logger.debug('Сброс параметров фильтрации')

        session = request.session
        FilterParametersTracking.delete(session=session)

        # Вывод товаров последней просматриваемой категории или тега
        category = ProductCategoryTracking.check(session=session)
        tag = ProductTagTracking.check(session=session)

        if category:
            return redirect(reverse('shop:products_list', kwargs={'category_name': category}))

        elif tag:
            return redirect(reverse('shop:filter_by_tags', kwargs={'tag_name': tag}))
