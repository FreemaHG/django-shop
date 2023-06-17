import logging

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
from .services.shop_cart.logic import CartProductsListService, CartProductsAddService
from .services.shop_cart.authenticated import ProductsCartUserService
from .services.orders_payment import Payment
from .services.products.search import ProductsListSearchService
from .services.products.browsing_history import ProductBrowsingHistoryService
from .services.main import ProductsForMainService
from .utils.input_data import clear_data
# from .utils.shop_cart import get_id_products_in_cart


logger = logging.getLogger(__name__)


class MainView(TemplateView):
    """
    Представление главной страницы сайта
    """

    template_name = '../templates/app_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = ProductsForMainService.save_data(context=context, request=self.request)

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

    # FIXME Перевести все в GET с выводом контекста (один метод) - стадия отладки!
    def get_queryset(self):
        """
        Вызов сервиса с бизнес-логикой для вывода товаров по переданным параметрам
        """
        logger.info(f'Новый запрос: {self.request.build_absolute_uri()}')

        # Сохраняем параметры фильтрации для передачи в контекст
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

        context['products_id'] = CartProductsListService.id_products(request=self.request)  # id товаров в корзине текущего пользователя

        # FIXME Попробовать заменить смену CSS при помощи JS!
        if self.filter_parameters:

            # Передача в шаблон параметров фильтрации
            context['filter_parameters'] = self.filter_parameters

            # Передача в шаблон индикатора сортировки
            sort_param = self.filter_parameters.get('sort', False)

            if not sort_param is False:
                context['filter_parameters']['sort'] = sort_param

                # Сортировка по цене
                if sort_param == 'by_price_down':
                    context['sorting_indicator_by_price'] = class_up  # Сортировка вверх

                elif sort_param == 'by_price_up':
                    context['sorting_indicator_by_price'] = class_down  # Сортировка вниз

                # Сортировка по популярности (кол-ву продаж)
                elif sort_param == 'by_popularity_down':
                    context['sorting_indicator_by_popularity'] = class_up

                elif sort_param == 'by_popularity_up':
                    context['sorting_indicator_by_popularity'] = class_down

                # Сортировка по отзывам
                elif sort_param == 'by_reviews_down':
                    context['sorting_indicator_by_reviews'] = class_up

                elif sort_param == 'by_reviews_up':
                    context['sorting_indicator_by_reviews'] = class_down

                # Сортировка по новизне
                elif sort_param == 'by_novelty_down':
                    context['sorting_indicator_by_novelty'] = class_up

                elif sort_param == 'by_novelty_up':
                    context['sorting_indicator_by_novelty'] = class_down

            logger.debug(f'Передача параметров в шаблон: {context["filter_parameters"]}')

        return context


class ProductsLisSearchView(ProductsListView):
    """
    Поиск товаров
    """
    def get_queryset(self):
        """
        Вывод товаров, найденных по поисковой фразе
        """
        current_url = self.request.build_absolute_uri()
        logger.info(f'Новый запрос: {current_url}')

        query = self.request.GET['query']
        logger.debug(f'Поиск товаров по фразе: {query}')

        products = ProductsListSearchService.search(query=query)

        # Сохраняем параметры фильтрации для передачи в контекст
        self.filter_parameters = self.kwargs | clear_data(self.request.GET)
        logger.info(f'Параметры фильтрации: {self.filter_parameters}')

        if 'sort' in current_url or 'filter' in current_url:
            products = ProductsListService.output(filter_parameters=self.filter_parameters, products=products)

        return products


class AboutView(View):
    """ Тестовая страница о магазине """
    def get(self, request):
        return render(request, '../templates/app_shop/about.html')


class ProductsSalesView(View):
    """
    Тестовая страница блога
    """
    def get(self, request):
        return render(request, '../templates/app_shop/sale.html')


class ProductDetailView(DetailView, FormMixin):
    """
    Детальная страница товара с комментариями
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
        self.object = cache.get_or_set(f'product_{id}', self.get_object(), 60 * config.caching_time)
        logger.info(f'Товар добавлен в кэш: id - {id}')

        context = self.get_context_data(object=self.object)
        comments = ProductCommentsService.all_comments(product=self.object)  # Комментарии к товару

        # id товаров в корзине текущего пользователя
        cart_products = CartProductsListService.id_products(request=self.request)

        context['cart_products'] = cart_products
        context['comments'] = comments[:1]
        context['total_comments'] = comments.count()

        # Сохранение истории просмотренных товаров
        ProductBrowsingHistoryService.save_view(request=request, product=self.object)

        return self.render_to_response(context)

    def post(self, request, pk):
        """
        Обработка формы с новым комментарием
        """
        form = CommentProductForm(request.POST)
        product = self.get_object()  # FIXME Извлекать объект из GET, проверить!!!
        comments = ProductCommentsService.all_comments(product=product)

        if form.is_valid():
            logger.debug(f'Данные формы валидны: {form.cleaned_data}')

            # Добавляем новый комментарий к товару
            result = ProductCommentsService.add_new_comments(
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

        return render(request, '../templates/app_shop/detail_product/product.html', context={
            'object': product,
            'comments': comments,
            'form': form
        })


def load_comments(request):
    """
    Загрузка доп.комментариев к товару
    """
    loaded_item = int(request.GET.get('loaded_item'))
    product_id = int(request.GET.get('product_id'))
    limit = 1

    comments = ProductReviews.objects.filter(product=product_id)[loaded_item:loaded_item+limit]
    comments_obj = []

    for comment in comments:
        comments_obj.append({
            'avatar': comment.buyer.profile.avatar.url,
            'name': comment.buyer.profile.full_name,
            'created_at': comment.created_at,
            'review': comment.review
        })

    data = {'comments': comments_obj}
    return JsonResponse(data=data)


def add_product(request):
    """
    Добавление товара в корзину
    """
    logger.debug('Добавление товара в корзину (Ajax-запрос)')
    res = CartProductsAddService.add(request=request)

    # logger.error(f'res: {res}')
    data = {'res': res}
    # data = {'res': False}  # Для тестирования сообщения об ошибке

    return JsonResponse(data=data)


def add_product_in_cart(request, **kwargs):
    """
    Добавление товара в корзину (перезагрузка страницы)
    """
    logger.debug('Добавление товара в корзину (с обновлением страницы)')
    CartProductsAddService.add(request=request, product_id=kwargs['product_id'])

    return HttpResponseRedirect(kwargs['next'])


def delete_product(request, **kwargs):
    """
    Удаление товара из корзины
    """
    logger.debug('Удаление товара из корзины (с обновлением страницы)')
    # TODO Возвращает res, который не используется
    CartProductsAddService.delete(request=request, product_id=kwargs['product_id'])

    return HttpResponseRedirect(kwargs['next'])


def reduce_product(request, **kwargs):
    """
    Уменьшение кол-ва товара в корзине
    """
    product_id = kwargs["product_id"]
    logger.debug(f'Уменьшение кол-ва товара в корзине: id - {product_id}')

    CartProductsAddService.reduce_product(request=request, product_id=product_id)

    return redirect('{}#{}'.format(reverse('shop:shopping_cart'), product_id))


def increase_product(request, **kwargs):
    """
    Увеличение кол-ва товара в корзине
    """
    product_id = kwargs["product_id"]
    logger.debug(f'Увеличение кол-ва товара в корзине: id - {product_id}')

    CartProductsAddService.increase_product(request=request, product_id=product_id)

    return redirect('{}#{}'.format(reverse('shop:shopping_cart'), product_id))


class ShoppingCartView(TemplateView):
    """
    Корзина с товарами пользователя
    """
    template_name = '../templates/app_shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # FIXME кэшировать данные
        records = CartProductsListService.output(self.request)
        context['records'] = records

        if records:
            total_cost = ProductsCartUserService.total_cost(records)
            context['total_cost'] = total_cost

        return context


class OrderRegistrationView(TemplateView):
    """
    Регистрация заказа
    """
    template_name = '../templates/app_shop/orders/registration/order.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод формы для оформления заказа
        """
        logger.debug('Регистрация заказа')
        context = self.get_context_data(**kwargs)

        if request.user.is_authenticated:
            logger.debug('Пользователь авторизован. Вывод формы для оформления заказа')
            form = MakingOrderForm()
            context['form'] = form
            records = CartProductsListService.output(self.request)
            context['records'] = records

            if records:
                total_cost = ProductsCartUserService.total_cost(records)
                context['total_cost'] = total_cost

            return self.render_to_response(context)
            # return render(request, '../templates/app_shop/orders/order.html', context={'form': form})

        else:
            logger.warning('Пользователь не авторизован. Вывод формы для регистрации')
            form = RegisterUserForm()
            context['form'] = form
            return self.render_to_response(context)
            # return render(request, '../templates/app_shop/orders/order.html', context={'form': form})

    def post(self, request):
        """
        Оплата заказа
        """
        logger.debug('Оплата заказа')
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
                # FIXME Вывод сообщения о неудачном оформлении заказа
                return HttpResponse('Какая-то ошибка при оформлении заказа')

        else:
            logger.error(f'Не валидные данные: {form.errors}')
            # FIXME Редирект на страницу с заказами с сообщением об ошибке
            return reverse('shop:order_registration')


class PaymentView(TemplateView):
    """
    Вывод и обработка формы для ввода номера карты (генерации случайного чужого счета) для оплаты заказа
    """
    template_name = '../templates/app_shop/orders/payment/payment.html'

    def post(self, request, *args, **kwargs):
        """
        Оплата заказа с номера введенной карты
        """
        logger.debug('Оплата заказа')
        order_id = kwargs['order_id']
        cart_number = request.POST['numero1']

        # Оплата заказа
        Payment.payment_processing(order_id=order_id, cart_number=cart_number)

        return redirect(reverse('shop:progress_payment', kwargs={'order_id': order_id}))
        # return redirect(reverse('shop:order_detail', kwargs={'order_id': order_id}))

# TODO Ожидание ассинхронного результата оплаты (с timeout!!!) с редиректом на страницу заказа
class ProgressPaymentView(TemplateView):
    """
    Вывод страницы ожидания оплаты заказа
    """
    template_name = '../templates/app_shop/orders/payment/progressPayment.html'

    # TODO Редирект на страницу заказа после получения результата оплаты
    # return redirect(reverse('shop:order_detail', kwargs={'pk': order_id}))


class HistoryOrderView(ListView):
    """
    Страница с заказами текущего пользователя
    """
    model = Order
    template_name = '../templates/app_shop/orders/historyorder.html'
    paginate_by = 4


class OrderInformationView(DetailView):
    """
    Детальная страница заказа
    """
    model = Order
    template_name = '../templates/app_shop/orders/oneorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        products = PurchasedProduct.objects.filter(order=self.object)
        context['products'] = products

        return context
