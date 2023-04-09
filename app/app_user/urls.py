from django.urls import path

from .views import (
    account_view,
    LogoutUserView,
    LoginUserView,
    PasswordRecovery,
    ProfileView,
    ProfileWithAvatarView,
    register_user_view
)


app_name = 'user'

urlpatterns = [
    path('registration/', register_user_view, name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('password_recovery/', PasswordRecovery.as_view(), name='password_recovery'),
    # path('update_account/', AccountView.as_view(), name='update_account'),
    path('account/', account_view, name='account'),  # Личный кабинет
    path('profile/', ProfileView.as_view(), name='profile'),  # Профиль
    path('profile_with_avatar/', ProfileWithAvatarView.as_view(), name='profile_with_avatar'),  # Профиль с аватаром
]
