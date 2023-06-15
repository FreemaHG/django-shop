import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail, BadHeaderError

from app_shop.services.shop_cart.logic import CartProductsAddService
from app_shop.services.products.browsing_history import ProductBrowsingHistoryServices
from .models import Profile
from .forms import RegisterUserForm, AuthUserForm, EmailForm
from .utils.save_new_user import save_username, cleaned_phone_data
from .utils.check_users import check_for_email
from .utils.password_recovery import password_generation
from django.conf import settings

from app_shop.services.orders import RegistrationOrder
from app_shop.models import ProductBrowsingHistory

logger = logging.getLogger(__name__)

# TODO При неуспешной транзакции ниже не выполняется запрос в base.html get_solo при извлечении данных о сайте (ошибка при выводе шаблона)
# @transaction.atomic
def register_user_view(request):
    """
    Регистрация пользователя в расширенной форме
    """
    logger.debug('Регистрация пользователя')

    if request.user.is_authenticated:
        logger.warning('Пользователь уже зарегистрирован')
        return redirect('user:account')

    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST, request.FILES)
            next_page = request.GET.get('next', False)

            logger.warning(f'next_page: {next_page}')

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
                    error_message = 'Пользователь с таким email уже зарегистрирован'

                    if next_page:
                        logger.debug(f'Возврат на страницу: {next_page}')

                        if next_page and 'order' in next_page:
                            return render(request, 'app_shop/orders/registration/order.html', {'form': form, 'error_message': error_message})

                        return redirect(next_page)

                    return render(request, 'app_user/registration.html', {'form': form, 'error_message': error_message})

                try:
                    Profile.objects.create(
                        user=user,
                        full_name=full_name,
                        phone_number=cleaned_phone,
                        avatar=avatar
                    )
                except IntegrityError:
                    logger.error(f'Регистрация - дублирующийся phone_number')
                    error_message = 'Пользователь с таким номером телефона уже зарегистрирован'

                    if next_page and 'order' in next_page:
                        logger.debug(f'Возврат на страницу: {next_page}')
                        return render(request, 'app_shop/orders/registration/order.html', {'form': form, 'error_message': error_message})

                    return render(request, 'app_user/registration.html', {'form': form, 'error_message': error_message})

                # Слияние корзин в БД
                CartProductsAddService.merge_carts(request=request, user=user)

                # Авторизация нового пользователя и редирект в личный кабинет
                user = authenticate(username=username, password=password)
                login(request, user)

                if next_page:
                    logger.debug(f'Возврат на страницу: {next_page}')
                    return redirect(next_page)

                return redirect('user:account')

            logger.error(f'Регистрация - не валидные данные: {form.errors}')

            if next_page and 'order' in next_page:
                logger.debug(f'Возврат на страницу: {next_page}')
                return render(request, 'app_shop/orders/registration/order.html', {'form': form})

            return render(request, 'app_user/registration.html', {'form': form})

        else:
            form = RegisterUserForm()

        return render(request, 'app_user/registration.html', {'form': form})


class LogoutUserView(LogoutView):
    """
    Выход из учетной записи
    """
    next_page = '/'


class LoginUserView(FormView):
    """
    Авторизация пользователя
    """
    form_class = AuthUserForm
    template_name = '../templates/app_user/account/login.html'

    @transaction.atomic
    def form_valid(self, form):
        logger.debug(f'Данные валидны: {form.cleaned_data}')

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = save_username(email)
        next_page = self.request.GET.get('next', False)

        try:
            user = authenticate(username=username, password=password)
            login(self.request, user)

            # Слияние корзин в БД
            CartProductsAddService.merge_carts(request=self.request, user=user)

            if next_page:
                logger.debug(f'Возврат на страницу: {next_page}')
                return redirect(next_page)

            return redirect('user:account')

        except AttributeError:
            return render(self.request, '../templates/app_user/account/login.html', {
                'form': form,
                'error_message': 'Email или пароль не верны!'
            })


class PasswordRecovery(FormView):
    """
    Восстановления пароля
    """
    form_class = EmailForm
    template_name = '../templates/app_user/account/password_recovery.html'

    def form_valid(self, form, message='', error_message=''):
        logger.debug(f'Данные валидны: {form.cleaned_data}')
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
                message = 'Новый пароль выслан на указанный Email.'

            except BadHeaderError:
                error_message = 'При отправке Email произошла ошибка! Попробуйте позже...'

        else:
            error_message = 'Пользователь с таким Email не найден!'

        return render(self.request, '../templates/app_user/account/password_recovery.html', {
            'form': form,
            'message': message,
            'error_message': error_message,
        })


def account_view(request):
    """
    Личный кабинет пользователя
    """
    logger.debug('Личный кабинет пользователя')

    if request.user.is_authenticated:
        last_order = RegistrationOrder.last_order(request=request)
        return render(request, '../templates/app_user/account/account.html', context={'last_order': last_order})

    return redirect('%s?next=%s' % (reverse('user:login'), request.path))


class ProfileView(View):
    """
    Профайл: редактирование данных пользователя
    """
    logger.debug('Профайл: редактирование данных пользователя')

    def get(self, request):
        if request.user.is_authenticated:
            form = RegisterUserForm()
            return render(request, '../templates/app_user/account/profile.html', {'form': form})

        return redirect('%s?next=%s' % (reverse('user:login'), request.path))


class UpdateAccountView(FormView):
    """
    Обновление данных пользователя
    """
    form_class = RegisterUserForm
    template_name = '../templates/app_user/account/profile.html'

    def form_valid(self, form, message='', error_message=''):
        logger.debug(f'Данные валидны: {form.cleaned_data}')

        user = self.request.user
        full_name = form.cleaned_data.get('full_name', False)
        email = form.cleaned_data.get('email', False)
        phone_number = form.cleaned_data.get('phone_number', None)
        avatar = self.request.FILES.get('avatar', False)

        username = save_username(email)  # Извлекаем и сохраняем username по email

        user.username = username
        user.email = email  # Обработать ошибку неуникального Email
        user.save()

        profile = Profile.objects.get(user=user)

        if full_name:
            profile.full_name=full_name

        if phone_number:
            cleaned_phone = cleaned_phone_data(phone_number)  # Очистка номера телефона
            profile.phone_number=cleaned_phone

        if avatar and not avatar is None:
            profile.avatar=avatar

        profile.save()

        message = 'Данные успешно обновлены'

        return render(self.request, '../templates/app_user/account/profile.html', {
            'form': form,
            'message': message
        })


class BrowsingHistoryView(ListView):
    """
    История просмотров
    """
    model = ProductBrowsingHistory
    template_name = '../templates/app_user/account/browsing_history.html'
    context_object_name = 'records'
    paginate_by = 8

    def get_queryset(self):
        records = ProductBrowsingHistoryServices.history_products(request=self.request)
        return records
