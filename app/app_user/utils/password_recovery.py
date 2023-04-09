import string
import secrets
import logging


logger = logging.getLogger(__name__)

def password_generation() -> str:
    """ Генерация нового случайного пароля """

    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(secrets.choice(alphabet) for i in range(8))
    logger.debug(f'Сгенерирован новый случайный пароль')

    return new_password
