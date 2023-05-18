import logging


logger = logging.getLogger(__name__)


def save_username(email: str) -> str:
    """ Функция принимает Email, извлекает и возвращает username """

    username = email.split('@')[0]
    return username


def cleaned_phone_data(phone: str):
    """
    Очищает входящую строку с номером от '+7' и возвращает None в случае пустой строки
    """

    if phone.startswith('+7'):
        return phone.split('+7')[1]

    if phone.startswith('+'):
        return phone.lstrip('+')

    elif not phone:
        return None

    else:
        return phone
