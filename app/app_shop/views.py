import logging

from django.http import HttpResponse
from django.views.generic import View, ListView
from django.shortcuts import render

from .services.products.products_list import ProductsList
from .models import Product, CategoryProduct


logger = logging.getLogger(__name__)

class MainView(View):
    """ Тестовая главная страница """
    def get(self, request):
        return render(request, '../templates/app_shop/index.html')


class ProductsListCategoryView(ListView):
    """
    Вывод товаров определенной категории
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    # paginate_by = 8  # Разбиение на страницы

    def get_queryset(self, **kwargs):
        """
        Извлечение названия категории из URL и вывод отфильтрованных товаров
        """
        logger.debug('Запуск представления')
        products = ProductsList.output_by_category(category_name=self.kwargs['category_name'])

        return products


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


class CatalogView(View):
    """ Тестовая страница с каталогом товаров """
    def get(self, request):
        return render(request, '../templates/app_shop/catalog.html')


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
