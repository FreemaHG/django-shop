import logging

from typing import Union
from django.core.exceptions import ObjectDoesNotExist

from ..models import CategoryProduct


logger = logging.getLogger(__name__)

class GetCategory:

    @classmethod
    def get_category_id(cls, category_name: str) -> Union[int, bool]:
        """
        Метод возвращает id категории по переданному полю slug
        """
        try:
            category_id = CategoryProduct.objects.only('id').get(slug=category_name)
            logger.info('Найден id категории')
            return category_id

        except ObjectDoesNotExist:
            logger.warning('id категории не найден')
            return False
