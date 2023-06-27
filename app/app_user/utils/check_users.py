import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


def check_for_email(email: str) -> bool | User:
    """
    Функция для поиска пользователя в БД по email

    @param email: строка с email
    @return: объект пользователя / False, если не найден
    """
    try:
        user = User.objects.get(email=email)
        logger.debug(f"Пользователь с email: {email} найден")

        return user

    except ObjectDoesNotExist:
        logger.warning(f"Пользователь с email: {email} не найден")

        return False
