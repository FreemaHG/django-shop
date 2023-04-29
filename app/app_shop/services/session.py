import logging

from typing import Union, Dict
from django.db.models import QuerySet
from django.contrib.sessions.models import Session


logger = logging.getLogger(__name__)

class ProductCategoryTracking:
    """
    Сервис по отслеживанию последней просматриваемой категории товаров текущего пользователя
    """

    @classmethod
    def add(cls, session: Session, category: Union[str, bool] = False) -> None:
        """
        Добавление новой записи в сессию о просматриваемой категории товаров
        """
        logger.info(f'Добавление категории товара в сессию: {category}')

        if category:
            session['last_category'] = category
        else:
            session['last_category'] = 'all'

    @classmethod
    def check(cls, session: Session) -> str:
        """
        Проверка последней записи в сессии о просматриваемой категории товаров
        """
        logger.debug('Извлечение записи из сессии о последней просматриваемой категории товаров')
        return session.get('last_category', False)

    @classmethod
    def delete(cls, session: Session):
        """
        Удаление записи о последней просматриваемой категории товаров
        """
        logger.debug('Удаление из сессии данных о последней просматриваемой категории товаров')

        try:
            del session['last_category']
        except KeyError:
            logger.warning('Данные нельзя удалить, т.к. они еще не были записаны')


class ProductTagTracking:
    """
    Сервис по отслеживанию текущим пользователем последних просматриваемых товаров определенного тега
    """

    @classmethod
    def add(cls, session: Session, tag: Union[str, bool] = False) -> None:
        """
        Добавление новой записи в сессию о просматриваемой категории товаров
        """
        logger.info(f'Добавление тега товара в сессию: {tag}')
        session['last_tag'] = tag

    @classmethod
    def check(cls, session: Session) -> str:
        """
        Проверка последней записи в сессии о просматриваемых товарах определенного тега
        """
        logger.debug('Извлечение записи из сессии о последних просматриваемых товарах определенного тега')
        return session.get('last_tag', False)

    @classmethod
    def delete(cls, session: Session):
        """
        Удаление записи о последних просматриваемых товарах определенного тега
        """
        logger.debug('Удаление из сессии данных о последних просматриваемых товарах определенного тега')

        try:
            del session['last_tag']
        except KeyError:
            logger.warning('Данные нельзя удалить, т.к. они еще не были записаны')


class FilterParametersTracking:
    """
    Сервис по отслеживанию параметров фильтрации товаров текущего пользователя
    """

    @classmethod
    def add(cls, filter_parameters: Dict, session: Session) -> None:
        """
        Добавление новой записи с параметрами фильтрации
        """
        logger.debug('Добавление записи в сессию о параметрах фильтрации')

        parameters_filter = {
            'price': {
                'min': filter_parameters['min_price'],
                'max': filter_parameters['max_price']
            },
            'title': filter_parameters['title'],
            'in_stock': filter_parameters['in_stock'],
            'free_shipping': filter_parameters['free_shipping']
        }
        session['filters'] = parameters_filter
        logger.debug(f'Проверка записи в сессии: {session["filters"]}')

    @classmethod
    def get(cls, session: Session) -> Dict:
        """
        Извлечение параметров фильтрации из объекта сессии текущего пользователя
        """
        logger.debug('Извлечение записи из сессии о параметрах фильтрации')
        parameters_filter = session.get('filters', False)
        return parameters_filter

    @classmethod
    def delete(cls, session: Session):
        """
        Удаление записи о параметрах фильтрации текущего пользователя
        """
        logger.debug('Удаление записи из сессии о параметрах фильтрации')

        try:
            session['filters'].clear()
        except KeyError:
            logger.warning('Данные нельзя удалить, т.к. они еще не были записаны')
