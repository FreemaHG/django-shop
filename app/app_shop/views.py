import logging

from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic import View, ListView
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .services.products.filter import ProductFilter
from .services.products.sorting import ProductSorted
from .models import Product, CategoryProduct, ProductTags
from .services.session import (
    ProductCategoryTracking,
    ProductTagTracking,
    FilterParametersTracking,
    SortProductsTracing,
    SortProductsTracingForPrice,
)


logger = logging.getLogger(__name__)

class MainView(View):
    """ Тестовая главная страница """
    def get(self, request):
        return render(request, '../templates/app_shop/index.html')


class ProductsListView(ListView):
    """
    Вывод каталога товаров (определенной категории или всех)
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self, **kwargs):
        logger.debug('Вывод товаров')

        session = self.request.session
        category_name = self.kwargs.get('category_name', False)
        logger.info(f'Извлечение категории товаров: {category_name}')

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
        logger.debug('Вывод товаров определенного тега')

        session = self.request.session
        tag_name = self.kwargs.get('tag_name', False)
        logger.info(f'Извлечение тега товаров: {tag_name}')

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
        filtered_products = ProductFilter.output_by_filter(session=session)

        logger.warning(f'Параметр сортировки ДО: {session["sorted"]}')

        if sorted_data:
            # Сортировка товаров по цене по возрастанию
            sorted_products = ProductSorted.by_price_up(products=filtered_products)

            logger.info('Меняем сортировку по цене на убывание')
            # Меняем сортировку на "по убыванию"
            SortProductsTracingForPrice.add_price_down(session=session)

            logger.warning(f'Параметр сортировки ПОСЛЕ: {session["sorted"]}')

        else:
            # Сортировка товаров по цене по убыванию
            sorted_products = ProductSorted.by_price_down(products=filtered_products)

            logger.debug('Меняем сортировку по цене на возрастание')
            # Устанавливаем сортировку на "по возрастанию"
            SortProductsTracingForPrice.add_price_up(session=session)

            logger.warning(f'Параметр сортировки ПОСЛЕ: {session["sorted"]}')

        # ОЧИСТКА всех параметров сортировки, КРОМЕ ЦЕНЫ
        # SortProductsTracing.clear_data(session=session, control_parameter='by_price')

        return sorted_products


class ProductsFilterListView(View):
    """
    Вывод отфильтрованных товаров
    """
    # paginate_by = 8  # Разбиение на страницы

    def post(self, request):
        logger.debug('Фильтрация товаров')

        session = request.session
        new_filter_parameters = {
            # 'price_range': request.POST.get('price', False),
            'min_price': request.POST.get('min_price', False),
            'max_price': request.POST.get('max_price', False),
            'title': request.POST.get('title', False),
            'in_stock': True if request.POST.get('in_stock', False) else False,
            'free_shipping': True if request.POST.get('free_shipping', False) else False,
        }

        logger.info(f'Переданные параметры: {new_filter_parameters}')

        # СОХРАНЕНИЕ параметров фильтрации текущего пользователя
        FilterParametersTracking.add(new_filter_parameters=new_filter_parameters, session=session)



        # FIXME Сделать один вызываемый метод для вывода товаров с заданными критериями по фильтрации и сортировке
        # Вывод отфильтрованных товаров
        res_products = ProductFilter.output_by_filter(session=session)


        # Вывод параметров фильтрации ТЕКУЩЕГО пользователя
        filter_parameters = FilterParametersTracking.get(session=session)

        logger.info(f'Параметры фильтрации, передаваемый в шаблон: {filter_parameters}')

        return render(request, '../templates/app_shop/catalog.html', {
            'products': res_products,
            'filter_parameters': filter_parameters,
        })


class ResetFiltersView(View):
    """
    Сброс параметров фильтрации
    """
    def get(self, request):
        logger.debug('Сброс параметров фильтрации')
        session = request.session
        FilterParametersTracking.delete(session=session)

        category = ProductCategoryTracking.check(session=session)
        tag = ProductTagTracking.check(session=session)

        if category:
            return redirect(reverse('shop:products_list', kwargs={'category_name': category}))

        elif tag:
            return redirect(reverse('shop:filter_by_tags', kwargs={'tag_name': tag}))


class AboutView(View):
    """ Тестовая страница о магазине """
    def get(self, request):
        return render(request, '../templates/app_shop/about.html')


class ProductsSalesView(View):
    """ Тестовая страница с распродажей товаров """
    def get(self, request):
        return render(request, '../templates/app_shop/sale.html')


class ProductDetailView(View):
    """ Тестовая страница товара """
    def get(self, request):
        return render(request, '../templates/app_shop/product.html')


class ShoppingCartView(View):
    """ Тестовая корзина с товарами """
    def get(self, request):
        return render(request, '../templates/app_shop/cart.html')


class OrderRegistrationView(View):
    """ Тестовая страница для регистрации заказа """
    def get(self, request):
        return render(request, '../templates/app_shop/orders/order.html')


class OrderInformationView(View):
    """ Тестовая страница с информацией о заказе """
    def get(self, request):
        return render(request, '../templates/app_shop/orders/oneorder.html')


class HistoryOrderView(View):
    """ Тестовая страница с историей заказов """
    def get(self, request):
        return render(request, '../templates/app_shop/orders/historyorder.html')


class PaymentView(View):
    """ Тестовая страница с оплатой """
    def get(self, request):
        return render(request, '../templates/app_shop/orders/payment/payment.html')


class PaymentWithInvoiceGenerationView(View):
    """ Тестовая страница с оплатой с генерацией случайного счета """
    def get(self, request):
        return render(request, '../templates/app_shop/orders/payment/paymentsomeone.html')


class ProgressPaymentView(View):
    """ Тестовая страница с ожиданием оплаты """
    def get(self, request):
        return render(request, '../templates/app_shop/orders/payment/progressPayment.html')
