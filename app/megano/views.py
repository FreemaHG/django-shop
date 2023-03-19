from django.views.generic import View
from django.shortcuts import render


class MainView(View):
    """ Тестовая главная страница """

    def get(self, request):
        return render(request, '../templates/index.html')
