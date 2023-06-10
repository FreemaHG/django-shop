from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .utils.save_new_user import cleaned_phone_data


class EmailForm(forms.Form):
    """
    Форма для восстановления пароля (ввода email)
    """
    email = forms.EmailField(label='E-mail', help_text='Введите email')


class AuthUserForm(EmailForm):
    """
    Форма авторизации пользователя
    """
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', help_text='Введите пароль')


class RegisterUserForm(UserCreationForm):
    """
    Расширенная форма для регистрации пользователя
    """
    full_name = forms.CharField(min_length=2, max_length=150, label='ФИО', help_text='Введите полное имя')
    email = forms.EmailField(label='E-mail', help_text='Введите корректный email')
    phone_number = forms.CharField(min_length=10, max_length=12, required=False, label='Телефон', help_text='Введите номер телефона')
    # phone_number = forms.NumberInput()
    avatar = forms.ImageField(required=False, label='Аватар', help_text='Выберите аватар')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль', help_text='Тут можно изменить пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля',
                                      help_text='Введите пароль повторно')


    # def clean_phone_number(self):
    #     """
    #     Проверка поля ввода номера телефона
    #     """
    #     input_phone = self.cleaned_data['phone_number']
    #
    #     cleaned_data = cleaned_phone_data(input_phone)
    #
    #     if not cleaned_data.isdigit():
    #         raise ValidationError('Номер телефона должен состоять из цифр!')


    def clean_password2(self):
        """
        Проверка, что введенные пароли совпадают
        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError('Пароли не совпадают!')

    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'phone_number', 'email', 'password1', 'password2']

        labels = {
            'email': 'E-mail',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
