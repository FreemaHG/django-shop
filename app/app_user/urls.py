from django.urls import path, re_path, include

from .views import (
    account_view,
    LogoutUserView,
    LoginUserView,
    PasswordRecovery,
    ProfileView,
    UpdateAccountView,
    ProfileWithAvatarView,
    register_user_view
)


app_name = 'user'

urlpatterns = [
    path('registration/', register_user_view, name='registration'),
    path('login/', include([
        path('', LoginUserView.as_view(), name='login'),
        re_path(r'^.*', LoginUserView.as_view(), name='login'),  # Обработка ?next
    ])),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('password_recovery/', PasswordRecovery.as_view(), name='password_recovery'),
    path('update_account/', UpdateAccountView.as_view(), name='update_account'),
    path('account/', account_view, name='account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_with_avatar/', ProfileWithAvatarView.as_view(), name='profile_with_avatar'),  # Профиль с аватаром
]
