import logging

from django.http import HttpRequest

from ..forms import MakingOrderForm


logger = logging.getLogger(__name__)


class RegistrationOrder:
    """
    Сервис для оформления заказа
    """

    @classmethod
    def create_order(cls, request: HttpRequest, form: MakingOrderForm) -> bool:
        """
        Создание заказа
        """
        logger.debug('Создание заказа')
        # full_name = form.cleaned_data.get('full_name', False)
        # phone_number = form.cleaned_data.get('phone_number', False)
        # email = form.cleaned_data.get('email', False)
        delivery = form.cleaned_data.get('delivery', False)
        city = form.cleaned_data.get('city', False)
        address = form.cleaned_data.get('address', False)
        pay = form.cleaned_data.get('pay', False)

        if delivery == 'ordinary':
            delivery_num = 1
        else:
            delivery_num = 2

        if pay == 'online':
            pay_num = 1
        else:
            pay_num = 2

        MakingOrderForm.objects.create(
            user=request.user,
            city=city,
            address=address,
            delivery=delivery_num,
            pay=pay_num
        )

    def payment(self):
        """
        Оплата заказа
        """
        ...

    def order_payment_status(self):
        """
        Получить статус оплаты заказа
        """
        ...
