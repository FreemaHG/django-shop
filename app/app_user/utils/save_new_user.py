import logging


logger = logging.getLogger(__name__)

def save_username(email: str) -> str:
    """ Функция принимает Email, извлекает и возвращает username """

    username = email.split('@')[0]
    return username
