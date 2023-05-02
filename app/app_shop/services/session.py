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
        if category:
            session['last_category'] = category
        else:
            session['last_category'] = 'all'

        logger.info(f'Сессия: добавление категории товара: {session["last_category"]}')

    @classmethod
    def check(cls, session: Session) -> str:
        """
        Проверка последней записи в сессии о просматриваемой категории товаров
        """
        last_category = session.get('last_category', False)
        logger.debug(f'Сессия: извлечение данных о категории: {last_category}')

        return last_category

    @classmethod
    def delete(cls, session: Session):
        """
        Удаление записи о последней просматриваемой категории товаров
        """
        logger.debug('Сессия: удаление категории')

        try:
            del session['last_category']
        except KeyError:
            logger.warning('Сессия: данные нельзя удалить, т.к. они еще не были записаны')


class ProductTagTracking:
    """
    Сервис по отслеживанию текущим пользователем последних просматриваемых товаров определенного тега
    """

    @classmethod
    def add(cls, session: Session, tag: Union[str, bool] = False) -> None:
        """
        Добавление новой записи в сессию о просматриваемой категории товаров
        """
        session['last_tag'] = tag
        logger.info(f'Сессия: добавление тега: {session["last_tag"]}')

    @classmethod
    def check(cls, session: Session) -> str:
        """
        Проверка последней записи в сессии о просматриваемых товарах определенного тега
        """
        last_tag = session.get('last_tag', False)
        logger.debug(f'Сессия: извлечение данных о теге: {last_tag}')

        return last_tag

    @classmethod
    def delete(cls, session: Session):
        """
        Удаление записи о последних просматриваемых товарах определенного тега
        """
        logger.debug('Сессия: удаление данных о товарах тега')

        try:
            del session['last_tag']
        except KeyError:
            logger.warning('Сессия: данные нельзя удалить, т.к. они еще не были записаны')


class FilterParametersTracking:
    """
    Сервис по отслеживанию параметров фильтрации товаров текущего пользователя
    """

    @classmethod
    def add(cls, new_filter_parameters: Dict, session: Session) -> None:
        """
        Добавление новой записи с параметрами фильтрации
        """
        logger.debug('Сессия: добавление параметров фильтрации')

        parameters_filter = cls.get(session=session)

        if not parameters_filter:
            logger.debug('Сессия: добавление НОВОЙ записи')
            logger.debug(f'Сессия: входные параметры: {new_filter_parameters}')

            parameters_filter = {
                'min_price': new_filter_parameters['min_price'],
                'max_price': new_filter_parameters['max_price'],
                'title': new_filter_parameters['title'],
                'in_stock': new_filter_parameters['in_stock'],
                'free_shipping': new_filter_parameters['free_shipping']
            }
            session['filters'] = parameters_filter

        else:
            logger.debug('Сессия: ОБНОВЛЕНИЕ записи')

            for key, value in new_filter_parameters.items():
                if session['filters'][key] != value:
                    session['filters'][key] = value

        logger.info(f'Сессия: обновленные данные фильтрации: {session["filters"]}')

    @classmethod
    def get(cls, session: Session) -> Dict:
        """
        Извлечение параметров фильтрации из объекта сессии текущего пользователя
        """
        parameters_filter = session.get('filters', False)
        logger.debug(f'Сессия: извлечение данных фильтрации: {parameters_filter}')
        return parameters_filter

    @classmethod
    def delete(cls, session: Session) -> None:
        """
        Удаление записи о параметрах фильтрации текущего пользователя
        """
        logger.info('Сессия: удаление данных фильтрации')

        try:
            del session['filters']

        except KeyError:
            logger.warning('Сессия: данные нельзя удалить, т.к. они еще не были записаны')


class SortProductsTracingForPrice:
    """
    Сервис по отслеживанию параметров сортировки товаров по цене для текущего пользователя
    """

    @classmethod
    def add_price_down(cls, session: Session) -> None:
        """
        Добавление новой записи с параметрами сортировки по цене (по убыванию)
        """
        # TODO Почему-то при проверке не то же самое, что при записи
        logger.info('Сессия: добавление записи о сортировке по цене (по убыванию)')
        session['sorted']['by_price'] = False

    @classmethod
    def add_price_up(cls, session: Session) -> None:
        """
        Добавление новой записи с параметрами сортировки по цене (по возрастанию)
        """
        logger.info('Сессия: добавление записи о сортировке по цене (по возрастанию)')
        session['sorted'] = {}
        session['sorted']['by_price'] = True

    @classmethod
    def check(cls, session: Session):
        """
        Проверка параметра сортировки по цене для текущего пользователя
        """
        try:
            check_data = session['sorted']['by_price']
            logger.debug(f'Сессия: параметр сортировки: {session["sorted"]}')

            return check_data

        except KeyError:
            logger.warning('Сессия: параметры сортировки по цене не найдены')
            return False


class SortProductsTracing:
    """
    Очистка параметров сортировки для текущего пользователя
    """

    @classmethod
    def check_or_create(cls, session: Session):
        """
        Проверка и создание ключа 'sorted' в сессии текущего пользователя, если такого нет
        """
        res = session.get('sorted', False)

        if not res:
            session['sorted'] = {}
            logger.info('Сессия: параметр сортировки создан')


    @classmethod
    def clear_data(cls, session: Session, control_parameter: str = 'None'):
        """
        Выборочная очистка ВСЕХ данных, кроме переданного параметра
        """
        logger.info(f'Сессия: очистка параметров сортировки, кроме {control_parameter}')

        sorted_parameters = session.get('sorted', False)

        if sorted_parameters:

            for parameter in sorted_parameters.keys():
                if parameter != control_parameter:
                    try:
                        del session[parameter]
                    except KeyError:
                        logger.warning(f'Сессия: параметр сортировки {parameter} не найден')
        else:
            logger.warning('Сессия: данные нельзя удалить, т.к. они еще не были записаны')


    @classmethod
    def delete(cls, session: Session):
        """
        Очистка всех параметров сортировки
        """
        try:
            logger.info(f'Сессия: очистка параметров сортировки')
            del session['sorted']

        except KeyError:
            logger.warning('Сессия: данные сортировки нельзя удалить, т.к. они еще не были записаны')
