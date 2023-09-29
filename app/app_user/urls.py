from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page

from app.config.utils.configuration import get_config
from app.app_user.views import (
    register_user_view,  # Регистрация пользователя
    LoginUserView,  # Авторизация
    LogoutUserView,  # Выход
    PasswordRecoveryView,  # Восстановление пароля
    account_view,  # Личный кабинет
    ProfileView,  # Профайл
    UpdateAccountView,  # Обновление данных аккаунта
    BrowsingHistoryView,  # История просмотров
)


app_name = "user"
config = get_config()  # Настройки сайта с параметрами кэширования

urlpatterns = [
    # Регистрация
    path(
        "registration/",
        include(
            [
                path(
                    "",
                    cache_page(60 * config.caching_time)(register_user_view),
                    name="registration",
                ),
                re_path(
                    r"^(?P<next>.*)", register_user_view, name="registration"
                ),  # Обработка ?next
            ]
        ),
    ),
    # Авторизация и выход
    path(
        "login/",
        include(
            [
                path(
                    "",
                    cache_page(60 * config.caching_time)(LoginUserView.as_view()),
                    name="login",
                ),
                re_path(
                    r"^(?P<next>.*)", LoginUserView.as_view(), name="login"
                ),  # Обработка ?next
            ]
        ),
    ),
    path(
        "logout/",
        cache_page(60 * config.caching_time)(LogoutUserView.as_view()),
        name="logout",
    ),
    # Восстановление пароля
    path(
        "password_recovery/",
        cache_page(60 * config.caching_time)(PasswordRecoveryView.as_view()),
        name="password_recovery",
    ),
    # Личный кабинет
    path("account/", account_view, name="account"),
    path("profile/", ProfileView.as_view(), name="profile"),
    # Обновление данных аккаунта
    path("update_account/", UpdateAccountView.as_view(), name="update_account"),
    # История просмотров
    path("browsing_history/", BrowsingHistoryView.as_view(), name="browsing_history"),
]
