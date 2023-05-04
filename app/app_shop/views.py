import logging

from django.http import HttpResponse
from django.views.generic import View, ListView
from django.shortcuts import render

from .models import Product
from .services.products.output_products import ProductsListService
from .utils.input_data import clear_data


logger = logging.getLogger(__name__)


class MainView(View):
    """ Тестовая главная страница """
    def get(self, request):
        return render(request, '../templates/app_shop/index.html')


class ProductsListView(ListView):
    """
    Вывод каталога товаров (определенной категории, тега или всех).
    Фильтрация и сортировка по переданным в URL параметрам.
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        """
        Вызов сервиса с бизнес-логикой для вывода товаров по переданным параметрам
        """
        logger.error(f'Новый запрос: {self.request.build_absolute_uri()}')

        self.filter_parameters = self.kwargs | clear_data(self.request.GET)
        logger.info(f'Параметры фильтрации: {self.filter_parameters}')

        products = ProductsListService.output(filter_parameters=self.filter_parameters)

        return products


    def get_context_data(self, **kwargs):
        """
        Передача в шаблон параметров вывода товаров
        """
        context = super().get_context_data(**kwargs)
        class_up = 'Sort-sortBy_dec'
        class_down = 'Sort-sortBy_inc'

        if self.filter_parameters:

            # Передача в шаблон параметров фильтрации
            context['filter_parameters'] = self.filter_parameters

            # Передача в шаблон индикатора сортировки
            sort_param = self.filter_parameters.get('sort', False)

            if not sort_param is False:
                context['filter_parameters']['sort'] = sort_param

                if sort_param == 'by_price_down':
                    context['sorting_indicator_by_price'] = class_up  # Сортировка вверх

                elif sort_param == 'by_price_up':
                    context['sorting_indicator_by_price'] = class_down  # Сортировка вниз

                elif sort_param == 'by_novelty_down':
                    context['sorting_indicator_by_novelty'] = class_up  # Сортировка вверх

                elif sort_param == 'by_novelty_up':
                    context['sorting_indicator_by_novelty'] = class_down  # Сортировка вниз

            logger.info(f'Передача параметров в шаблон: {context["filter_parameters"]}')

        return context


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
