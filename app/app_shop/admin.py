import json
import logging

from django.contrib import admin, messages
from django.db.models import JSONField
from mptt.admin import DraggableMPTTAdmin
from mptt.querysets import TreeQuerySet

from .models import CategoryProduct, Product, ProductTags, ProductImages, ProductReviews, Cart
from .utils.admin.change_status_delete import soft_deletion_child_records


logger = logging.getLogger(__name__)


@admin.action(description='Мягкое удаление всех записей (включая дочерние)')
def deleted_all_records(adminmodel, request, queryset):
    """
    Мягкое удаление всех записей, включая дочерние
    """
    soft_deletion_child_records(queryset)  # Мягкое удаление всех дочерних записей
    queryset.update(deleted=True)  # Мягкое удаление родительской записи


@admin.action(description='Мягкое удаление')
def deleted_records(adminmodel, request, queryset):
    """
    Мягкое удаление всех записей, включая дочерние
    """
    queryset.update(deleted=True)  # Мягкое удаление родительской записи


@admin.action(description='Восстановить записи')
def restore_records(adminmodel, request, queryset):
    """
    Восстановить записи, отключенные ч/з мягкое удаление
    """
    queryset.update(deleted=False)  # Восстановление родительской записи


@admin.action(description='Перевести в "Избранные категории"')
def make_selected(adminmodel, request, queryset):
    """
    Перевод категорий в избранные
    """
    queryset.update(selected=True)


@admin.action(description='Удалить из "Избранные категории"')
def remove_selected(adminmodel, request, queryset):
    """
    Перевод категорий в избранные
    """
    queryset.update(selected=False)


@admin.register(CategoryProduct)
class CategoryProductAdmin(DraggableMPTTAdmin):
    """
    Админ-панель для категорий товаров
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'slug', 'selected', 'deleted')
    list_display_links = ('indented_title',)
    list_filter = ('selected', 'deleted')
    list_editable = ('deleted',)
    search_fields = ('title',)
    # Мягкое удаление/восстановление записей, перевод и удаление из избранных
    actions = (deleted_all_records, restore_records, make_selected, remove_selected)

    fieldsets = (
        ('Основное', {'fields': ('title', 'parent')}),
        ('Файлы', {'fields': ('icon', 'image')}),
        ('Статусы', {'fields': ('selected', 'deleted')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Проверяем уровень вложенности категории перед сохранением
        """

        if obj.parent:
            max_indent = 2
            lvl = obj.parent.level + 1

            if lvl < max_indent:
                super(CategoryProductAdmin, self).save_model(request, obj, form, change)
            else:
                messages.set_level(request, messages.ERROR)  # Меняем уровень сообщения на ERROR
                # Чтобы избежать вывода одновременно 2 сообщений: успешного и в случае ошибки
                messages.add_message(
                    request,
                    level=messages.ERROR,
                    message=f'Превышена максимальная вложенность категорий в {max_indent} уровня! '
                            f'Текущая вложенность: {lvl + 1}'
                )
        else:
            super(CategoryProductAdmin, self).save_model(request, obj, form, change)


@admin.register(ProductTags)
class ProductTagsAdmin(admin.ModelAdmin):
    """
    Админ-панель для товарных тегов
    """
    list_display = ('id', 'name', 'slug', 'deleted')
    list_display_links = ('name',)
    list_editable = ('deleted',)
    actions = (deleted_records, restore_records)  # Мягкое удаление/восстановление записей

    fieldsets = (
        ('Основное', {'fields': ('name', 'slug', 'deleted')}),
    )


class ChoiceImages(admin.TabularInline):
    """
    Вывод изображений на странице товара
    """
    model = ProductImages
    extra = 1


class ChoiceReviews(admin.TabularInline):
    """
    Вывод комментариев на странице товара
    """
    model = ProductReviews
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель для товаров
    """
    list_display = ('id', 'short_name', 'category', 'price', 'discount', 'count', 'limited_edition', 'created_at', 'deleted')
    list_display_links = ('short_name',)
    list_filter = ('limited_edition', 'category', 'tags')
    search_fields = ('name',)
    list_editable = ('deleted',)
    actions = (deleted_records, restore_records)  # Мягкое удаление/восстановление записей
    inlines = (ChoiceImages, ChoiceReviews)

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'definition', 'characteristics'),
            'description': 'Название и описание товара',
        }),
        ('Категория и теги', {'fields': ('category', 'tags')}),
        ('Стоимость и скидка', {'fields': ('price', 'discount')}),
        ('Кол-во товара', {
            'fields': ('count', 'limited_edition'),
            'description': 'Оставшееся кол-во товара на складе, а также принадлежность товара к ограниченному тиражу',
        }),
        ('Статус', {
            'fields': ('deleted',),
            'description': 'Статус товара: активен или удален из БД',
            'classes': ('collapse',)
        }),
    )

    def short_name(self, obj):
        """
        Возврат короткого названия товара (не более 150 символов)
        """
        if len(obj.name) > 150:
            return f'{obj.name[0:150]}...'

        return obj.name

    short_name.short_description = 'Название товара'


@admin.register(ProductReviews)
class ProductReviewsAdmin(admin.ModelAdmin):
    """
    Админ-панель для комментариев к товарам
    """
    list_display = ('product_name', 'buyer', 'short_review', 'created_at', 'deleted')
    list_display_links = ('product_name',)
    list_filter = ('deleted',)
    search_fields = ('product', 'short_review')
    list_editable = ('deleted',)
    actions = (deleted_records, restore_records)  # Мягкое удаление/восстановление записей

    def short_review(self, obj):
        """
        Возврат короткого отзыва (не более 250 символов)
        """
        if len(obj.review) > 250:
            return f'{obj.review[0:250]}...'
        return obj.review

    short_review.short_description = 'Отзыв'

    def product_name(self, obj):
        """
        Возврат короткого названия товара (не более 100 символов)
        """
        if len(obj.product.name) > 50:
            return f'{obj.product.name[0:50]}...'
        return obj.product.name

    product_name.short_description = 'Товар'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Админ-панель для карты с товарами пользователя
    """
    # readonly_fields = ['buyer', 'product_name']

    list_display = ('id', 'full_name', 'product_id', 'product_name', 'price', 'count', 'discount', 'position_cost')
    list_display_links = ('id',)
    search_fields = ('user__profile__full_name', 'product__name')

    def full_name(self, obj):
        """
        Полное имя покупателя
        """
        return obj.user.profile.full_name

    full_name.short_description = 'Покупатель'

    def product_name(self, obj):
        """
        Человекопонятное название товара
        """
        limit = 100
        product_name = obj.product.name

        if len(product_name) > limit:
            return obj.product.name[:limit] + '...'

        return product_name

    def product_id(self, obj):
        """
        id товара
        """
        return obj.product.id

    product_id.short_description = 'id товара'

    def price(self, obj):
        """
        Цена товара (без учета скидки)
        """
        return obj.product.price

    price.short_description = 'Цена, руб'

    def discount(self, obj):
        """
        Скидка на товар
        """
        return obj.product.discount

    discount.short_description = 'Скидка, %'

    def position_cost(self, obj):
        """
        Стоимость позиции товара с учетом скидки и кол-ва товара
        """
        return obj.position_cost

    position_cost.short_description = 'Стоимость позиции, руб'

    def get_readonly_fields(self, request, obj=None):
        """
        Запрещаем редактиваровать поля с товаром и покупателем
        """
        if obj:
            return ['full_name', 'product_name', 'count']

        return self.readonly_fields

    fieldsets = (
        ('Запись о товаре в корзине', {
            'fields': ('full_name', 'product_name', 'count'),
            'description': 'Покупатель, товар и кол-во товара',
        }),
    )
