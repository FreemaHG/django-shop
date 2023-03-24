from django.shortcuts import render
from django.views import View


class AccountView(View):
    """ Тестовая страница личного кабинета """
    def get(self, request):
        return render(request, '../templates/app_user/account/account.html')


class ProfileView(View):
    """ Тестовая страница с данными пользователя """
    def get(self, request):
        return render(request, '../templates/app_user/account/profile.html')


class ProfileWithAvatarView(View):
    """ Тестовая страница с данными пользователя 2 """
    def get(self, request):
        return render(request, '../templates/app_user/account/profileAvatar.html')
