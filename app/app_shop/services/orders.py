
class RegistrationOrder:
    """
    Сервис для оформления заказа
    """

    def user_parameters(self):
        """
        Подстановка и сохранение параметров пользователя
        """
        ...

    def delivery_method(self):
        """
        Выбор способа доставки
        """
        ...

    def payment_method(self):
        """
        Выбор способа оплаты
        """
        ...

    def confirmation(self):
        """
        Подтверждение заказа
        """
        ...

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
