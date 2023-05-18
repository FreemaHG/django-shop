import logging

from typing import Union
from django.core.exceptions import ObjectDoesNotExist

from ..models import ProductTags


logger = logging.getLogger(__name__)

class GetTag:

    @classmethod
    def get_tag_id(cls, tag_name: str) -> Union[int, bool]:
        """
        Метод возвращает id тега по переданному полю slug
        """
        logger.debug(f'Утилиты: поиск тега по переданному значению: {tag_name}')

        try:
            tag_id = ProductTags.objects.only('id').get(slug__icontains=tag_name)
            logger.info(f'Тег найден. id - {tag_id}')
            return tag_id

        except ObjectDoesNotExist:
            logger.warning('Тег не найден')
            return False
