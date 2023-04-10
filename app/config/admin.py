from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from solo.admin import SingletonModelAdmin

from .models import SiteConfiguration


admin.site.register(SiteConfiguration, SingletonModelAdmin)

try:
    # Получить один имеющийся элемент из таблицы можно следующим образом
    config = SiteConfiguration.objects.get()

except OperationalError or ObjectDoesNotExist:
    config = SiteConfiguration.get_solo()  # get_solo создаст элемент, если он не существует
