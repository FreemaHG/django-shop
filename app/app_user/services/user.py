import logging
from typing import Union, Tuple, Any

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, BadHeaderError
from django.db import IntegrityError
from django.core.mail import send_mail, BadHeaderError

from ..models import Profile
from ..forms import RegisterUserForm, EmailForm, AuthUserForm
from ..utils.save_new_user import save_username, cleaned_phone_data
from ..utils.check_users import check_for_email
from ..utils.password_recovery import password_generation
from app_shop.services.shop_cart.logic import CartProductsAddService


logger = logging.getLogger(__name__)


class UserRegistrationService:
    """
    Сервис для регистрации, обновления данных и вывода информации о пользователе
    """

    @classmethod
    def registration(cls, request: HttpRequest) -> Any:
        """ Регистрация нового пользователя """

        _ERROR_MESSAGE_EMAIL = 'Пользователь с таким email уже зарегистрирован'
        _ERROR_MESSAGE_PHONE = 'Пользователь с таким номером телефона уже зарегистрирован'

        form = RegisterUserForm(request.POST, request.FILES)
        next_page = request.GET.get('next', False)

        if form.is_valid():
            logger.debug(f'Данные валидны: {form.cleaned_data}')
            user = form.save(commit=False)
            full_name = form.cleaned_data.get('full_name', False)
            email = form.cleaned_data.get('email', False)
            phone_number = form.cleaned_data.get('phone_number', None)
            avatar = request.FILES.get('avatar', None)
            password = form.cleaned_data.get('password1')

            username = save_username(email)  # Извлекаем и сохраняем username по email
            user.username = username
            cleaned_phone = cleaned_phone_data(phone_number)  # Очистка номера телефона

            try:
                user.set_password(password)
                user.save()

            except IntegrityError:
                logger.error(f'Регистрация - дублирующийся email')

                return next_page, form, _ERROR_MESSAGE_EMAIL

            try:
                Profile.objects.create(
                    user=user,
                    full_name=full_name,
                    phone_number=cleaned_phone,
                    avatar=avatar
                )

            except IntegrityError:
                logger.error(f'Регистрация - дублирующийся phone_number')
                return next_page, form, _ERROR_MESSAGE_PHONE

            # Слияние корзин в БД
            CartProductsAddService.merge_carts(request=request, user=user)

            # Авторизация нового пользователя
            user = authenticate(username=username, password=password)
            login(request, user)

            return next_page, form, False

        else:
            logger.error(f'Регистрация - не валидные данные: {form.errors}')

            return next_page, form, False


    @classmethod
    def login(cls, request: HttpRequest, form : AuthUserForm) -> Any:
        """
        Метод для авторизации пользователя

        @param request: объект http-запроса
        @param form: форма для ввода логина и пароля
        @return: сообщение об успешной/неуспешной отправке инструкций на указанный Email
        """
        logger.debug('Авторизация пользователя')

        _ERROR_MESSAGE = 'Email или пароль не верны!'

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = save_username(email)
        next_page = request.GET.get('next', False)

        try:
            user = authenticate(username=username, password=password)
            login(request, user)

            # Слияние корзин в БД
            CartProductsAddService.merge_carts(request=request, user=user)

            if next_page:
                logger.debug(f'Возврат на страницу: {next_page}')
                return next_page, False, False

            logger.debug('Перенаправление в личный кабинет')
            return False, True, False

        except AttributeError:
            logger.warning('Email или пароль не верны!')
            return False, False, _ERROR_MESSAGE


    @classmethod
    def password_recovery(cls, form: EmailForm) -> Tuple[str, str]:
        """
        Метод для восстановления пароля пользователя

        @param form: форма для ввода Email
        @return: сообщение об успешной/неуспешной отправке инструкций на указанный Email
        """
        _MESSAGE = 'Новый пароль выслан на указанный Email'
        _ERROR_MESSAGE = 'При отправке Email произошла ошибка! Попробуйте позже...'
        _ERROR_MESSAGE_NOT_USER = 'Пользователь с таким Email не найден!'

        logger.debug('Восстановление пароля пользователя')

        email = form.cleaned_data.get('email')
        user = check_for_email(email)

        if user:
            new_password = password_generation()
            user.set_password(new_password)
            user.save()
            logger.info(f'Пароль для пользователя username: {user.username} id: {user.id} успешно изменен')

            try:
                send_mail(
                    f'{email} от Megano',
                    f'Новый пароль - {new_password}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )

                logger.info('Сообщение в новым паролем успешно отправлено пользователю')
                return _MESSAGE, ''

            except BadHeaderError:
                return '', _ERROR_MESSAGE

        else:
            logger.warning(f'Пользователь с Email: {email} не найден')
            return '', _ERROR_MESSAGE_NOT_USER


    @classmethod
    def editing_data(cls, request: HttpRequest, form: RegisterUserForm) -> Tuple[str, str]:
        """
        Метод для редактирования данных о пользователе

        @param request: объект http-запроса
        @param form: форма с новыми данными
        @return: сообщение об успешном/неуспешном обновлении данных
        """
        logger.debug('Редактирование данных пользователя')

        _MESSAGE = 'Данные успешно обновлены'
        _ERROR_MESSAGE_EMAIL = 'Указанный Email уже используется другим пользователем'
        _ERROR_MESSAGE_PHONE = 'Указанный номер телефона уже используется другим пользователем'

        user = request.user
        full_name = form.cleaned_data.get('full_name', False)
        email = form.cleaned_data.get('email', False)
        phone_number = form.cleaned_data.get('phone_number', None)
        avatar = request.FILES.get('avatar', False)

        username = save_username(email)  # Извлекаем и сохраняем username по email

        try:
            user.username = username
            user.email = email
            user.save()

        except IntegrityError:
            return '', _ERROR_MESSAGE_EMAIL

        profile = Profile.objects.get(user=user)

        if full_name:
            profile.full_name = full_name

        if phone_number:
            cleaned_phone = cleaned_phone_data(phone_number)  # Очистка номера телефона
            profile.phone_number = cleaned_phone

        if avatar and not avatar is None:
            profile.avatar = avatar

        try:
            profile.save()

        except IntegrityError:
            return '', _ERROR_MESSAGE_PHONE

        return _MESSAGE, ''
