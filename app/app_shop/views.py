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
    Вывод каталога товаров определенной категории
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    # paginate_by = 8  # Разбиение на страницы

    def get_queryset(self, **kwargs):
        """
        Извлечение названия категории из URL и вывод отфильтрованных товаров
        """
        logger.debug('Запуск представления ProductsListCategoryView')
        products = ProductsList.output_by_category(category_name=self.kwargs['category_name'])

        # FIXME Сохранить товары в текущей сессии для последующей фильтрации
        # if products:  # Сохраняем товары в текущей сессии для последующей возможной фильтрации
        #     self.request.session['products'] = list(products)

        return products


class ProductsFilterListView(View):
    """
    Вывод отфильтрованных товаров
    """
    # paginate_by = 8  # Разбиение на страницы

    def post(self, request):
        logger.debug('Запуск представления ProductsFilterListView')

        # FIXME Извлечение товаров из текущей сесии для фильтрации
        try:
            products = request.session.get('products')
            logger.debug(f'Товары из сессии: {products}')

        except KeyError:
            products = Product.objects.all()

        res_products = ProductsList.output_by_filter(context_data=request.POST)
        # res_products = ProductsList.output_by_filter(context_data=request.POST, products=products)

        # TODO После вывода отфильтрованных товаров в блоке фильтра сохраняются выставленные значения
        return render(request, '../templates/app_shop/catalog.html', {'products': res_products})


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
