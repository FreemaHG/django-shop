from django.urls import path, re_path, include

from .views import (
    register_user_view,  # Регистрация пользователя
    LoginUserView,  # Авторизация
    LogoutUserView,  # Выход
    PasswordRecoveryView,  # Восстановление пароля

    account_view,  # Личный кабинет
    ProfileView,  # Профайл
    UpdateAccountView,  # Обновление данных аккаунта
    BrowsingHistoryView,  # История просмотров
)


app_name = 'user'

urlpatterns = [
    # Регистрация
    path('registration/', include([
        # TODO Убрать лишние!!
        path('', register_user_view, name='registration'),
        # path('<str:next_page>/', register_user_view, name='registration'),
        # re_path(r'^.*', register_user_view, name='registration'),  # Обработка ?next
        # re_path(r'^(?P<next_page>.*)', register_user_view, name='registration'),  # Обработка ?next
        re_path(r'^(?P<next>.*)', register_user_view, name='registration'),  # Обработка ?next
    ])),

    # Авторизация и выход
    path('login/', include([
        path('', LoginUserView.as_view(), name='login'),
        # TODO Убрать лишние!!
        # re_path(r'^.*', LoginUserView.as_view(), name='login'),  # Обработка ?next
        re_path(r'^(?P<next>.*)', LoginUserView.as_view(), name='login'),  # Обработка ?next
    ])),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),  # Восстановление пароля

    # Личный кабинет
    path('account/', account_view, name='account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_account/', UpdateAccountView.as_view(), name='update_account'),  # Обновление данных аккаунта
    path('browsing_history/', BrowsingHistoryView.as_view(), name='browsing_history'),  # История просмотров
]
