from django.contrib import admin

from .models import Profile, Seller, Buyer
from .utils.models.output import output_name


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Профайл пользователя """

    list_display = ['user', 'name', 'phone_number', 'address']
    list_display_links = ['user', 'name']
    search_fields = ['user']

    def name(self, object):
        return output_name(object)

    name.short_description = 'Имя'


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """ Продавец """

    list_display = ['title', 'description']
    list_display_links = ['title']
    search_fields = ['title']


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    """ Покупатель """

    list_display = ['profile']
    list_display_links = ['profile']
    search_fields = ['profile']
