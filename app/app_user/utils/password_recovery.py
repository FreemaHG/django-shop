import string
import secrets
import logging


logger = logging.getLogger(__name__)


def password_generation() -> str:
    """
    Функция для генерации случайного 8-ми значного пароля

    @return: строка - рандомный пароль
    """
    alphabet = string.ascii_letters + string.digits
    new_password = "".join(secrets.choice(alphabet) for i in range(8))

    logger.info(f"Сгенерирован новый случайный пароль")

    return new_password
