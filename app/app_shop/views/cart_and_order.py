import logging
from typing import List, Dict

from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.shortcuts import render, redirect

from app_user.forms import RegisterUserForm
from ..models.cart_and_orders import Order
from ..forms import MakingOrderForm
from ..services.orders import RegistrationOrder
from ..services.shop_cart.logic import CartProductsListService
from ..services.shop_cart.authenticated import ProductsCartUserService
from ..services.orders_payment import Payment


logger = logging.getLogger(__name__)


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
