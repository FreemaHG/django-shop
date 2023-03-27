from django.contrib import admin, messages
from mptt.admin import DraggableMPTTAdmin

from .models import CategoryProduct
from .utils.admin.change_status_delete import soft_deletion_child_records


@admin.action(description='Удалить (мягкое удаление)')
def deleted_records(adminmodel, request, queryset):
    """ Мягкое удаление записей """

    soft_deletion_child_records(queryset)  # Мягкое удаление всех дочерних записей
    queryset.update(deleted=True)  # Мягкое удаление родительской записи


@admin.action(description='Восстановить записи')
def restore_records(adminmodel, request, queryset):
    """ Восстановить записи, отключенные ч/з мягкое удаление """

    queryset.update(deleted=False)  # Восстановление родительской записи


@admin.register(CategoryProduct)
class CategoryProductAdmin(DraggableMPTTAdmin):
    """ Админ-панель модели категории товаров """

    list_display = ('tree_actions', 'indented_title', 'selected', 'deleted')
    list_display_links = ('indented_title',)
    list_filter = ('selected', 'deleted')
    list_editable = ('deleted',)
    search_fields = ('title',)
    prepopulated_field = {'slug': ('title',)}
    actions = [deleted_records, restore_records]  # Мягкое удаление/восстановление записей

    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'parent')}),
        ('Файлы', {'fields': ('icon', 'image')}),
        ('Статусы', {'fields': ('selected', 'deleted')}),
    )

    def save_model(self, request, obj, form, change):
        """ Проверяем уровень вложенности категории перед сохранением """

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
