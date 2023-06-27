import logging

from typing import Union
from django.core.exceptions import ObjectDoesNotExist

from ..models.products import CategoryProduct


logger = logging.getLogger(__name__)


class GetCategoryUtil:
    @classmethod
    def get_category_id(cls, category_name: str) -> Union[int, bool]:
        """
        Метод возвращает id категории по переданному полю slug

        @param category_name: название категории
        @return: id категории / False, если категория не найдена
        """
        logger.debug(f"Поиск категории по переданному значению: {category_name}")

        try:
            category_id = CategoryProduct.objects.only("id").get(slug=category_name)
            logger.debug(f"Категория найдена. id - {category_id}")

            return category_id

        except ObjectDoesNotExist:
            logger.warning("Категория не найдена")

            return False
