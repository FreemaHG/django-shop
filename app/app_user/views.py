import logging

from django.contrib.auth.views import LogoutView
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.views import View

from app_shop.services.products.browsing_history import ProductBrowsingHistoryService
from app_shop.services.orders import RegistrationOrder
from app_shop.models.products import ProductBrowsingHistory
from .forms import RegisterUserForm, AuthUserForm, EmailForm
from .services.user import UserRegistrationService


logger = logging.getLogger(__name__)


# TODO При неуспешной транзакции ниже не выполняется запрос в base.html get_solo при извлечении данных о сайте (ошибка при выводе шаблона)
# @transaction.atomic
def register_user_view(request):
    """
    Представление для регистрации пользователя в расширенной форме
    """
    logger.debug('Регистрация пользователя')

    if request.user.is_authenticated:
        logger.warning('Пользователь уже зарегистрирован')
        return redirect('user:account')

    else:
        if request.method == 'POST':
            next_page, form, error_message = UserRegistrationService.registration(request=request)

            if error_message or form.errors:
                if next_page:
                    if 'order' in next_page:
                        return render(request, 'app_shop/orders/registration/order.html', {'form': form, 'error_message': error_message})

                return render(request, 'app_user/registration.html', {'form': form, 'error_message': error_message})

            if next_page:
                return redirect(next_page)
            else:
                return redirect('user:account')
        else:
            form = RegisterUserForm()

        return render(request, 'app_user/registration.html', {'form': form})


class LogoutUserView(LogoutView):
    """
    Представление для выхода из учетной записи
    """
    next_page = '/'


class LoginUserView(FormView):
    """
    Представление для авторизации пользователя
    """
    form_class = AuthUserForm
    template_name = '../templates/app_user/account/login.html'

    @transaction.atomic
    def form_valid(self, form, error_message=''):
        logger.debug(f'Данные валидны: {form.cleaned_data}')

        next_page, account, error_message = UserRegistrationService.login(request=self.request, form=form)

        if next_page:
            logger.info(f'Возврат на страницу: {next_page}')
            return redirect(next_page)

        elif account:
            logger.info('Перенаправление в личный кабинет')
            return redirect('user:account')

        else:
            return render(self.request, '../templates/app_user/account/login.html', {
                'form': form,
                'error_message': error_message
            })


class PasswordRecovery(FormView):
    """
    Представление для восстановления пароля от личного кабинета пользователя
    """
    form_class = EmailForm
    template_name = '../templates/app_user/account/password_recovery.html'

    def form_valid(self, form, message='', error_message=''):
        logger.debug(f'Данные валидны: {form.cleaned_data}')
        message, error_message = UserRegistrationService.password_recovery(form=form)

        return render(self.request, '../templates/app_user/account/password_recovery.html', {
            'form': form,
            'message': message,
            'error_message': error_message,
        })


def account_view(request):
    """
    Обработка запроса для вывода личного кабинета пользователя
    """
    if request.user.is_authenticated:
        logger.debug('Вывод личного кабинета пользователя')
        last_order = RegistrationOrder.last_order(request=request)

        logger.warning(f'last_order: {last_order}')

        return render(request, '../templates/app_user/account/account.html', context={'last_order': last_order})

    logger.warning('Пользователь не авторизован. Перенаправление на страницу авторизации')
    return redirect('%s?next=%s' % (reverse('user:login'), request.path))


class ProfileView(View):
    """
    Представление для вывода формы для редактирования данных пользователя
    """
    def get(self, request):
        logger.debug('Вывод формы для редактирования данных пользователя')

        if request.user.is_authenticated:
            form = RegisterUserForm()
            return render(request, '../templates/app_user/account/profile.html', {'form': form})

        logger.warning('Пользователь не авторизован. Перенаправление на страницу авторизации')
        return redirect('%s?next=%s' % (reverse('user:login'), request.path))


class UpdateAccountView(FormView):
    """
    Представление для обновления данных пользователя
    """
    form_class = RegisterUserForm
    template_name = '../templates/app_user/account/profile.html'

    def form_valid(self, form, message='', error_message=''):
        logger.debug(f'Данные валидны: {form.cleaned_data}')
        message, error_message = UserRegistrationService.editing_data(request=self.request, form=form)

        return render(self.request, '../templates/app_user/account/profile.html', {
            'form': form,
            'message': message,
            'error_message': error_message,
        })


class BrowsingHistoryView(ListView):
    """
    Представление для вывода истории просмотренных товаров пользователем
    """
    model = ProductBrowsingHistory
    template_name = '../templates/app_user/account/browsing_history.html'
    context_object_name = 'records'
    paginate_by = 8

    def get_queryset(self):
        records = ProductBrowsingHistoryService.history_products(request=self.request)
        return records
