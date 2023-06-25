import logging

from typing import Any
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ...models import Profile


logger = logging.getLogger(__name__)


class ProfileUtil:
    """
    Проверка и возврат профайла пользователя
    """

    @classmethod
    def get(cls, user: User) -> bool | Profile:
        """
        Метод для проверки на наличие профайла в БД

        @param user: объект пользователя
        @return: объект профайла / False, если не найден
        """
        logger.debug('Поиск профиля в БД по объекту User')

        try:
            profile = Profile.objects.get(user=user)
            logger.debug(f'Профиль найден: id - {profile.id} ({profile.full_name})')
            return profile

        except ObjectDoesNotExist:
            logger.warning('Профиль не найден')
            return False
