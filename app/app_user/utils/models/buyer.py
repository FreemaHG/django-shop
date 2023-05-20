import logging

from django.core.exceptions import ObjectDoesNotExist

from ...models import Buyer, Profile


logger = logging.getLogger(__name__)


class BuyerUtils:
    """
    Проверка и возврат объекта покупателя
    """
    @classmethod
    def get(cls, profile: Profile):
        """
        Проверка на наличие профайла в БД
        """
        logger.debug('Поиск объекта "Покупатель" в БД по профилю')

        try:
            buyer = Buyer.objects.get(profile=profile)
            logger.debug(f'Покупатель найден: id - {buyer.id})')

            return buyer

        except ObjectDoesNotExist:
            logger.warning('Покупатель не найден')

            return False
