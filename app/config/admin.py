from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from solo.admin import SingletonModelAdmin

from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):

    # Описываем поля для группировки
    fieldsets = (
        ('Ключевые параметры', {
            'fields': ('title', 'description', 'site_url', 'logo_head', 'logo_footer'),
            'description': 'Название, описание, URL и логотипы, размещаемые в шапке и футере сайта',
        }),
        ('Товары', {
            'fields': ('selected_products',),
            'description': 'Определение категорий избранных товаров, которые будут отображаться на главной '
                           'в блоке избранных товаров',
        }),
        ('Стоимость доставки', {
            'fields': ('shipping_cost', 'extra_shipping_cost', 'min_order_cost'),
            'description': 'Стоимость обычной и экспресс-доставки, установка минимальной стоимости заказа '
                           '/ товаров для бесплатной доставки',
        }),
        ('Кэш и режим работы', {
            'fields': ('caching_time', 'maintenance_mode'),
            'description': 'Настройки кэша и смена режима работы сайта',
        }),
    )

try:
    # Получить один имеющийся элемент из таблицы можно следующим образом
    config = SiteConfiguration.objects.get()

except OperationalError or ObjectDoesNotExist:
    config = SiteConfiguration.get_solo()  # get_solo создаст элемент, если он не существует
