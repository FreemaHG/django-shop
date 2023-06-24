import logging

from typing import Dict


logger = logging.getLogger(__name__)


def clear_data(data: Dict) -> Dict:
    """
    Функция для очистки входных данных (извлечение единичных значений из списков)

    @param data: словарь с данными
    @return: очищенный словарь с данными
    """
    cleared_data = {}

    for key, value in data.items():
        cleared_data[key] = value

    logger.debug(f'Данные после очистки: {cleared_data}')

    return cleared_data
