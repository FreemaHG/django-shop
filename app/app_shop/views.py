import logging

from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic import View, ListView
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .services.products.filter import ProductFilter
from .services.products.sorting import ProductSorted
from .services.session import ProductCategoryTracking, ProductTagTracking, FilterParametersTracking
from .models import Product, CategoryProduct, ProductTags


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
    # paginate_by = 8  # Разбиение на страницы

    def get_queryset(self, **kwargs):
        logger.debug('Вывод товаров')

        session = self.request.session
        category_name = self.kwargs.get('category_name', False)
        logger.info(f'Извлечение категории товаров: {category_name}')

        # Фиксируем в сессии просматриваемую категорию товаров
        ProductCategoryTracking.add(session=session, category=category_name)

        # Удаляем из сессии данные о последних просматриваемых товарах определенного тега
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

        # Фиксируем в сессии просматриваемую товары определенного тега
        ProductTagTracking.add(session=session, tag=tag_name)

        # Удаляем из сессии данные о последней просматриваемой категории товаров текущего пользователя
        ProductCategoryTracking.delete(session=session)

        # Товары нужной категории
        products = ProductFilter.output_by_tag(tag_name=tag_name)

        return products


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
            'in_stock': request.POST.get('in_stock', False),
            'free_shipping': request.POST.get('free_shipping', False),
        }

        # Вывод отфильтрованных товаров
        res_products = ProductFilter.output_by_filter(filter_parameters=new_filter_parameters, session=session)

        # Сохранение параметров фильтрации текущего пользователя
        FilterParametersTracking.add(filter_parameters=new_filter_parameters, session=session)

        # Вывод параметров фильтрации текущего пользователя
        filter_parameters = FilterParametersTracking.get(session=session)

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


class ProductsSortedByPrice(ListView):
    """
    Вывод товаров отсортированных по цене
    """
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        logger.debug('Запуск представления ProductsSortedByPrice')

        products = ProductCategoryTracking.check(session=self.request.session)

        if not products:
            logger.warning('В сессии пользователя не найдено данных о просматриваемой категории товаров')
            products = Product.objects.all()

        price_up = self.request.session.get('price_up', False)

        if price_up:
            sorted_products = ProductSorted.by_price_up(products)
            self.request.session['price_up'] = False
        else:  # Если флаг False
            sorted_products = ProductSorted.by_price_down(products)
            self.request.session['price_up'] = True

        return sorted_products


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
