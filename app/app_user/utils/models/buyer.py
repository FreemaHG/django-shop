import logging

from django.core.exceptions import ObjectDoesNotExist

from app.app_user.models import Buyer, Profile


logger = logging.getLogger(__name__)


class BuyerUtil:
    """
    Проверка и возврат объекта покупателя
    """

    @classmethod
    def get(cls, profile: Profile) -> bool | Buyer:
        """
        Метод для проверки на наличие профайла в БД

        @param profile: объект профайла
        @return: объект покупателя / False, если не найден
        """
        logger.debug('Поиск объекта "Покупатель" в БД по профилю')

        try:
            buyer = Buyer.objects.get(profile=profile)
            logger.debug(f"Покупатель найден: id - {buyer.id})")

            return buyer

        except ObjectDoesNotExist:
            logger.warning("Покупатель не найден")

            return False
