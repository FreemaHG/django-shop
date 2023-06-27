from django import forms


class CommentProductForm(forms.Form):
    """
    Форма для добавления нового комментария к товару
    """

    review = forms.CharField(
        max_length=2500, label="Комментарий", help_text="Оставьте ваш комментарий"
    )
    name = forms.CharField(max_length=200, label="Имя", help_text="Имя")
    email = forms.EmailField(label="Email", help_text="Email")


class MakingOrderForm(forms.Form):
    """
    Форма для оформления заказа
    """

    full_name = forms.CharField(
        max_length=150, label="ФИО", help_text="Введите полное имя"
    )
    phone_number = forms.CharField(
        min_length=10,
        max_length=12,
        label="Телефон",
        help_text="Введите номер телефона",
    )
    email = forms.EmailField(label="E-mail", help_text="Введите корректный email")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Пароль",
        help_text="Тут можно изменить пароль",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Подтверждение пароля",
        help_text="Введите пароль повторно",
    )
    delivery = forms.CharField(max_length=100)  # Тип доставки
    city = forms.CharField(
        max_length=100, label="Город", help_text="Введите город доставки"
    )
    address = forms.CharField(
        max_length=500, label="Адрес", help_text="Введите точный адрес доставки"
    )
    pay = forms.CharField(max_length=100)  # Вариант оплаты

    def clean(self):
        """
        Проверка идентичности введенных паролей
        """
        cleaned_data = super().clean()
        password1 = cleaned_data["password1"]
        password2 = cleaned_data["password2"]

        if password1 != password2:
            error_message = "Пароли не совпадают!"
            self.add_error("password1", error_message)
            self.add_error("password2", error_message)

        return cleaned_data
