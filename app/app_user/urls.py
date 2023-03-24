from django.urls import path

from .views import AccountView, ProfileView, ProfileWithAvatarView

app_name = 'user'

urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),  # Личный кабинет
    path('profile/', ProfileView.as_view(), name='profile'),  # Профайл
    path('profile_with_avatar/', ProfileWithAvatarView.as_view(), name='profile_with_avatar'),  # Профайл 2
]
