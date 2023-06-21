import logging
from typing import List, Dict

from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin
from django.core.cache import cache

from config.admin import config
from app_user.forms import RegisterUserForm
from .models import Product, ProductReviews, Order, PurchasedProduct
from .forms import CommentProductForm, MakingOrderForm
from .services.orders import RegistrationOrder
from .services.products.output_products import ProductsListService
from .services.products.detail_page import ProductCommentsService
from .services.products.products_list.filter import ProductFilter
from .services.products.products_list.sorting import ProductSort
from .services.shop_cart.logic import CartProductsListService, CartProductsAddService
from .services.shop_cart.authenticated import ProductsCartUserService
from .services.orders_payment import Payment
from .services.products.search import ProductsListSearchService
from .services.products.browsing_history import ProductBrowsingHistoryService
from .services.main import ProductsForMainService
from .utils.input_data import clear_data
from .services.products.context import SaveContextDataService
# from .utils.shop_cart import get_id_products_in_cart


logger = logging.getLogger(__name__)


class MainView(TemplateView):
    """
    Представление для вывода главной страницы сайта
    """
    template_name = '../templates/app_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = ProductsForMainService.save_data(context=context, request=self.request)

        return context


class BaseListView(ListView):
    """
    Базовое представление для вывода списка товаров (используется в ProductsListView и ProductsLisSearchView)
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        """
        Передача в шаблон параметров вывода товаров
        """
        context = super().get_context_data(**kwargs)
        context = SaveContextDataService.save_data(context=context, filter_parameters=self.filter_parameters, request=self.request)

        return context


class ProductsListView(BaseListView):
    """
    Представление для вывода каталога товаров (определенной категории, тега или всех).
    Фильтрация и сортировка по переданным в URL параметрам.
    """

    def get_queryset(self):
        """
        Вызов сервиса с бизнес-логикой для вывода товаров по переданным параметрам
        """
        logger.info(f'Новый запрос: {self.request.build_absolute_uri()}')

        # Сохраняем параметры фильтрации
        self.filter_parameters = self.kwargs | clear_data(self.request.GET)
        logger.info(f'Параметры фильтрации: {self.filter_parameters}')

        # Фильтрация по категории / тегу
        products = ProductsListService.output(filter_parameters=self.filter_parameters)

        # Фильтрация по переданным в форме параметрам
        products = ProductFilter.output(products=products, filters=self.filter_parameters)

        # Сортировка по переданным параметрам
        products = ProductSort.output(products=products, filters=self.filter_parameters)

        return products


class ProductsLisSearchView(BaseListView):
    """
    Представление для вывода найденных товаров по фразе в поисковой строке
    """

    def get_queryset(self) -> QuerySet:
        """
        Вывод товаров, найденных по поисковой фразе
        @return: список с товарами
        """
        logger.info(f'Новый запрос: {self.request.build_absolute_uri()}')

        # Сохраняем параметры фильтрации
        self.filter_parameters = self.kwargs | clear_data(self.request.GET)
        logger.info(f'Параметры фильтрации: {self.filter_parameters}')

        # Поиск товаров по названию
        products = ProductsListSearchService.search(request=self.request)

        # Фильтрация по переданным в форме параметрам
        products = ProductFilter.output(products=products, filters=self.filter_parameters)

        # Сортировка по переданным параметрам
        products = ProductSort.output(products=products, filters=self.filter_parameters)

        return products


class AboutView(TemplateView):
    """
    Представление для вывода страницы с информацией о магазине
    """
    template_name = '../templates/app_shop/about.html'


class ProductsSalesView(TemplateView):
    """
    Представление для вывода страницы блога
    """
    template_name = '../templates/app_shop/sale.html'


class ProductDetailView(DetailView, FormMixin):
    """
    Представление для вывода детальной страницы товара с комментариями
    """
    model = Product
    form_class = CommentProductForm
    template_name = '../templates/app_shop/detail_product/product.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод детальной страницы товара с комментариями
        """
        id = self.kwargs["pk"]  # id товара из URL

        # Возвращаем объект из кэша / кэшируем объект
        # (кэш товара автоматически очищается в model.save() при редактировании товара)
        self.object = cache.get_or_set(f'product_{id}', self.get_object(), 60 * config.caching_time)

        context = self.get_context_data(object=self.object)
        comments = ProductCommentsService.all_comments(product=self.object)  # Комментарии к товару

        # id товаров в корзине текущего пользователя
        # (для корректного отображения кнопки добавления товара/перехода в корзину)
        cart_products = CartProductsListService.id_products(request=self.request)

        context['cart_products'] = cart_products
        context['comments'] = comments[:1]
        context['total_comments'] = comments.count()

        # Добавление записи в истории просмотра авторизованного пользователя
        if request.user.is_authenticated:
            ProductBrowsingHistoryService.save_view(request=request, product=self.object)

        return self.render_to_response(context)

    def post(self, request, pk):
        """
        Валидация и обработка данных формы с новым комментарием к товару
        """
        form = CommentProductForm(request.POST)
        product = self.get_object()
        comments = ProductCommentsService.all_comments(product=product)

        if form.is_valid():
            logger.debug(f'Данные формы валидны: {form.cleaned_data}')

            result = ProductCommentsService.add_new_comments(
                form=form,
                product=product,
                user=request.user
            )

            if result:
                return HttpResponseRedirect(reverse('shop:product_detail', kwargs={'pk': pk}))
            else:
                logger.error(f'Ошибка при публикации комментария')
                return HttpResponse('При публикации комментария произошла ошибка, попробуйте позже...')

        else:
            logger.warning(f'Невалидные данные: {form.errors}')

            return render(request, '../templates/app_shop/detail_product/product.html', context={
                'object': product,
                'comments': comments,
                'total_comments': comments.count(),
                'form': form
            })


def load_comments(request):
    """
    Обработка запроса для загрузки доп.комментариев к товару
    """
    comments_obj = ProductCommentsService.load_comment(request=request)
    data = {'comments': comments_obj}

    return JsonResponse(data=data)


def add_product(request):
    """
    Обработка Ajax-запроса на добавление товара в корзину
    """
    logger.debug('Добавление товара в корзину (Ajax-запрос)')
    res = CartProductsAddService.add(request=request)
    data = {'res': res}

    return JsonResponse(data=data)


def add_product_in_cart(request, **kwargs):
    """
    Обработка запроса на добавление товара в корзину (с перезагрузкой страницы)
    """
    logger.debug('Добавление товара в корзину (с обновлением страницы)')
    CartProductsAddService.add(request=request, product_id=kwargs['product_id'])

    return HttpResponseRedirect(kwargs['next'])


def delete_product(request, **kwargs):
    """
    Обработка запроса на удаление товара из корзины
    """
    logger.debug('Удаление товара из корзины')
    CartProductsAddService.delete(request=request, product_id=kwargs['product_id'])

    return HttpResponseRedirect(kwargs['next'])


def reduce_product(request, **kwargs):
    """
    Обработка запроса на уменьшение кол-ва товара в корзине
    """
    product_id = kwargs["product_id"]
    logger.debug(f'Уменьшение кол-ва товара в корзине: id - {product_id}')
    CartProductsAddService.reduce_product(request=request, product_id=product_id)

    return redirect('{}#{}'.format(reverse('shop:shopping_cart'), product_id))


def increase_product(request, **kwargs):
    """
    Обработка запроса на увеличение кол-ва товара в корзине
    """
    product_id = kwargs["product_id"]
    logger.debug(f'Увеличение кол-ва товара в корзине: id - {product_id}')
    CartProductsAddService.increase_product(request=request, product_id=product_id)

    return redirect('{}#{}'.format(reverse('shop:shopping_cart'), product_id))


class ShoppingCartView(TemplateView):
    """
    Представление для вывода корзины с товарами пользователя
    """
    template_name = '../templates/app_shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = CartProductsListService.output(self.request)

        if records:
            context['records'] = records
            total_cost = ProductsCartUserService.total_cost(records)
            context['total_cost'] = total_cost

        return context


class OrderRegistrationView(TemplateView):
    """
    Представление для вывода и обработки формы при регистрации заказа
    """
    template_name = '../templates/app_shop/orders/registration/order.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод формы для оформления заказа для авторизованного пользователя
        либо формы для регистрации для неавторизованного.
        """
        context = self.get_context_data(**kwargs)

        if request.user.is_authenticated:
            logger.debug('Вывод формы для оформления заказа')
            context['form'] = MakingOrderForm()
            records = CartProductsListService.output(request=request)

            if records:
                context['records'] = records
                total_cost = ProductsCartUserService.total_cost(records)
                context['total_cost'] = total_cost

            return self.render_to_response(context)

        else:
            logger.warning('Пользователь не авторизован. Вывод формы для регистрации пользователя')
            context['form'] = RegisterUserForm()

            return self.render_to_response(context)

    def post(self, request):
        """
        Проверка и обработка входных данных, регистрация заказа, перенаправление на страницу ввода реквизитов
        """
        form = MakingOrderForm(request.POST)

        if form.is_valid():
            logger.debug(f'Данные формы валидны: {form.cleaned_data}')

            # Регистрация заказа
            order = RegistrationOrder.create_order(request=request, form=form)

            if order:
                logger.info('Заказ успешно оформлен')

                if order.payment == 1:
                    logger.debug('Перенаправление на страницу ввода номера карты')
                    return redirect(reverse('shop:online_payment', kwargs={'order_id': order.id}))

                else:
                    logger.debug('Перенаправление на страницу генерации случайного чужого счета')
                    return redirect(reverse('shop:someone_payment', kwargs={'order_id': order.id}))

            else:
                logger.error('Ошибка при оформлении заказа')
                return HttpResponse('При оформлении заказа произошла ошибка, попробуйте позже...')

        else:
            logger.error(f'Не валидные данные: {form.errors}')
            return reverse('shop:order_registration')


class PaymentView(TemplateView):
    """
    Представление для вывода и обработки формы для ввода номера карты
    (генерации случайного чужого счета) для оплаты заказа
    """
    template_name = '../templates/app_shop/orders/payment/payment.html'

    def post(self, request, **kwargs):
        """
        Вызов метода для оплаты заказа с номера введенной карты.
        Перенаправление на страницу-загрушки для ожидания фиктивной оплаты.
        """
        order_id = kwargs['order_id']
        cart_number = request.POST['numero1']

        Payment.payment_processing(order_id=order_id, cart_number=cart_number)

        return redirect(reverse('shop:progress_payment', kwargs={'order_id': order_id}))


class ProgressPaymentView(View):
    """
    Представление для вывода заглушки, имитирующей ожидание от сервиса оплаты.
    Автоматический редирект на страницу заказа через 4 сек при помощи JS-скрипта.
    """

    def get(self, request, **kwargs):
        order_id = kwargs['order_id']
        return render(request, '../templates/app_shop/orders/payment/progressPayment.html', {'order_id': order_id})


class HistoryOrderView(ListView):
    """
    Представление для вывода страницы с заказами текущего пользователя
    """
    model = Order
    template_name = '../templates/app_shop/orders/historyorder.html'
    paginate_by = 4


class OrderInformationView(DetailView):
    """
    Представление для вывода детальной страницы заказа
    """
    model = Order
    template_name = '../templates/app_shop/orders/oneorder.html'

    def get_context_data(self, **kwargs):
        """
        Сохранение в контексте товаров текущего заказа для вывода в шаблоне
        """
        context = super().get_context_data(**kwargs)
        context = RegistrationOrder.save_order_products_in_context(context=context, order=self.get_object())

        return context
