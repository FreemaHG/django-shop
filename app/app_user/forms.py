from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


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
    full_name = forms.CharField(min_length=2, max_length=150, label='ФИО')
    email = forms.EmailField(label='E-mail')
    phone_number = forms.CharField(min_length=10, max_length=12, required=False, label='Телефон')
    avatar = forms.ImageField(required=False, label='Аватар', help_text='Выберите аватар')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль', help_text='Тут можно изменить пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля',
                                      help_text='Введите пароль повторно')

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
