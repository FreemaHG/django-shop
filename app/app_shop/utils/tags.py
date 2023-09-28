import logging

from typing import Union
from django.core.exceptions import ObjectDoesNotExist

from app.app_shop.models.products import ProductTags


logger = logging.getLogger(__name__)


class GetTagUtil:
    @classmethod
    def get_tag_id(cls, tag_name: str) -> Union[int, bool]:
        """
        Метод возвращает id тега по переданному полю slug

        @param tag_name: название тега
        @return: id тега / False, если тег не найден
        """
        logger.debug(f"Поиск тега по переданному значению: {tag_name}")

        try:
            tag_id = ProductTags.objects.only("id").get(slug__icontains=tag_name)
            logger.info(f"Тег найден. id - {tag_id}")

            return tag_id

        except ObjectDoesNotExist:
            logger.warning("Тег не найден")

            return False
