from django.contrib import admin

from .models import Profile, Seller, Buyer
from .utils.models.output import output_name


@admin.action(description="Мягкое удаление")
def deleted_records(adminmodel, request, queryset):
    """
    Мягкое удаление всех записей, включая дочерние
    """
    queryset.update(deleted=True)  # Мягкое удаление родительской записи


@admin.action(description="Восстановить записи")
def restore_records(adminmodel, request, queryset):
    """
    Восстановить записи, отключенные ч/з мягкое удаление
    """
    queryset.update(deleted=False)  # Восстановление родительской записи


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профайл пользователя"""

    list_display = ["user", "name", "email", "phone_number", "address", "deleted"]
    list_display_links = ["user", "name"]
    search_fields = ["user"]
    actions = (
        deleted_records,
        restore_records,
    )  # Мягкое удаление/восстановление записей

    def name(self, object):
        return output_name(object)

    name.short_description = "Имя"

    def email(self, object):
        return object.user.email

    email.short_description = "Email"


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """Продавец"""

    list_display = ["title", "description", "deleted"]
    list_display_links = ["title"]
    search_fields = ["title"]
    actions = (
        deleted_records,
        restore_records,
    )  # Мягкое удаление/восстановление записей


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    """Покупатель"""

    list_display = ["profile", "deleted"]
    list_display_links = ["profile"]
    search_fields = ["profile"]
    actions = (
        deleted_records,
        restore_records,
    )  # Мягкое удаление/восстановление записей
