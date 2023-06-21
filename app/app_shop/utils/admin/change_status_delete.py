import logging

from django.db.models import QuerySet

from ...models.products import CategoryProduct


logger = logging.getLogger(__name__)

def soft_deletion_child_records(queryset: QuerySet):
    """
    Мягкое удаление дочерних записей
    """
    logger.debug('Утилиты: мягкое удаление дочерних записей')

    deleted_objects = []

    for record in queryset:
        children = record.get_descendants(include_self=False)  # Получаем все дочерние записи

        for child in children:
            child.deleted = True
            deleted_objects.append(child)

    # Сохраняем все измененные дочерние записи change_status_delete(queryset, True)
    CategoryProduct.objects.bulk_update(deleted_objects, ['deleted'])
