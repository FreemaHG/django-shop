import logging


logger = logging.getLogger(__name__)


def save_username(email: str) -> str:
    """
    Функция принимает Email, извлекает и возвращает username

    @param email: строка - email
    @return: строка - username
    """
    username = email.split('@')[0]

    return username


def cleaned_phone_data(phone: str) -> str | bool:
    """
    Функция очищает входящую строку с номером от '+7' и возвращает False в случае пустой переданной строки

    @param phone: строка - номер телефона
    @return: строка - очищенный номер телефона / False, если передана пустая строка
    """
    logger.debug(f'Очистка номера телефона. Передана строка: {phone}')

    if phone.startswith('+7'):
        return phone.split('+7')[1]

    if phone.startswith('+'):
        return phone.lstrip('+')

    elif not phone:
        return False

    else:
        return phone
