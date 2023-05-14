import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.core.cache import cache
from config.admin import config

from .models import Product
from .forms import CommentProductForm
from .services.products.output_products import ProductsListService
from .services.products.main import ProductsForMainService
from .services.products.detail_page import DetailProduct
from .utils.input_data import clear_data


logger = logging.getLogger(__name__)


class MainView(TemplateView):
    """
    Главная страница
    """
    template_name = '../templates/app_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_categories'] = ProductsForMainService.selected_categories()
        context['limited_products'] = ProductsForMainService.limited_edition()

        # FIXME Добавить после реализации механики покупки товаров
        # context['popular_products'] = ProductsForMainService.popular_products()
        context['popular_products'] = Product.objects.all()[:8]

        return context


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

            logger.debug(f'Передача параметров в шаблон: {context["filter_parameters"]}')

        return context


class AboutView(View):
    """ Тестовая страница о магазине """
    def get(self, request):
        return render(request, '../templates/app_shop/about.html')


class ProductsSalesView(View):
    """ Тестовая страница с распродажей товаров """
    def get(self, request):
        return render(request, '../templates/app_shop/sale.html')


class ProductDetailView(DetailView, FormMixin):
    """
    Детальная страница товара с комментариями.
    """
    model = Product
    form_class = CommentProductForm
    template_name = '../templates/app_shop/product.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод детальной страницы товара с комментариями
        """
        id = self.kwargs["pk"]  # id товара из URL

        # Возвращаем объект из кэша / кэшируем объект
        self.object = cache.get_or_set(f'product_{id}', self.get_object(), 60 * config.caching_time)
        logger.info(f'Товар добавлен в кэш: id - {id}')

        context = self.get_context_data(object=self.object)
        comments = DetailProduct.all_comments(product=self.object)  # Комментарии к товару
        context['comments'] = comments

        return self.render_to_response(context)


    def post(self, request, pk):
        """
        Обработка формы с новым комментарием
        """
        form = CommentProductForm(request.POST)
        product = self.get_object()  # FIXME Извлекать объект из GET, проверить!!!
        comments = DetailProduct.all_comments(product=product)

        if form.is_valid():
            logger.debug(f'Данные формы валидны: {form.cleaned_data}')

            # Добавляем новый комментарий к товару
            result = DetailProduct.add_new_comments(
                form=form,
                product=product,
                user=request.user
            )

            if result:
                return HttpResponseRedirect(reverse('shop:product_detail', kwargs={'pk': pk}))
                # return redirect(reverse(reverse('shop:product_detail', kwargs={'pk': pk, 'tag': 'comment'})))

            else:
                logger.error(f'Ошибка при публикации комментария')

        else:
            logger.warning(f'Невалидные данные: {form.errors}')

        return render(request, '../templates/app_shop/product.html', context={
            'object': product,
            'comments': comments,
            'form': form
        })


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
