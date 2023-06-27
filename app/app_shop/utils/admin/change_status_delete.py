import logging

from typing import List

from ...models.products import CategoryProduct


logger = logging.getLogger(__name__)


def soft_deletion_child_records(categories: List[CategoryProduct]) -> None:
    """
    Мягкое удаление дочерних категорий (смена статуса на неактивный)

    @param categories: список с категориями товаров
    @return: None
    """
    logger.debug("Мягкое удаление дочерних записей")

    deleted_objects = []

    for record in categories:
        children = record.get_descendants(
            include_self=False
        )  # Получаем все дочерние записи

        for child in children:
            child.deleted = True
            deleted_objects.append(child)

    # Сохраняем все измененные дочерние записи change_status_delete(queryset, True)
    CategoryProduct.objects.bulk_update(deleted_objects, ["deleted"])
