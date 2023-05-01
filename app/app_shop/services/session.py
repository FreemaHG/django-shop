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
    def add(cls, new_filter_parameters: Dict, session: Session) -> None:
        """
        Добавление новой записи с параметрами фильтрации
        """
        logger.debug('Добавление записи в сессию о параметрах фильтрации')

        parameters_filter = cls.get(session=session)

        if not parameters_filter:
            logger.warning('В текущей сессии нет записей с параметрами фильтрации. Добавление НОВОЙ записи')

            parameters_filter = {
                'min_price': new_filter_parameters['min_price'],
                'max_price': new_filter_parameters['max_price'],
                'title': new_filter_parameters['title'],
                'in_stock': new_filter_parameters['in_stock'],
                'free_shipping': new_filter_parameters['free_shipping']
            }
            session['filters'] = parameters_filter

        else:
            logger.info('ОБНОВЛЕНИЕ записи с параметрами фильтрации')

            for key, value in new_filter_parameters.items():
                if session['filters'][key] != value:
                    session['filters'][key] = value

    @classmethod
    def get(cls, session: Session) -> Dict:
        """
        Извлечение параметров фильтрации из объекта сессии текущего пользователя
        """
        logger.debug('Извлечение записи из сессии о параметрах фильтрации')
        parameters_filter = session.get('filters', False)
        return parameters_filter

    @classmethod
    def delete(cls, session: Session) -> None:
        """
        Удаление записи о параметрах фильтрации текущего пользователя
        """
        logger.debug('Удаление записи из сессии о параметрах фильтрации')

        try:
            session['filters'].clear()
        except KeyError:
            logger.warning('Данные нельзя удалить, т.к. они еще не были записаны')


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
        logger.debug('Добавление записи в сессию о параметре сортировки по цене (по убыванию)')
        session['sorted']['by_price'] = False
        logger.error(f'Проверка сортировки по цене: {session["sorted"]["by_price"]}')

    @classmethod
    def add_price_up(cls, session: Session) -> None:
        """
        Добавление новой записи с параметрами сортировки по цене (по возрастанию)
        """
        # TODO Почему-то при проверке не то же самое, что при записи
        logger.debug('Добавление записи в сессию о параметре сортировки по цене (по возрастанию)')
        session['sorted'] = {}
        session['sorted']['by_price'] = True
        logger.debug(f'Проверка сортировки по возрастанию: {session["sorted"]["by_price"]}')

    @classmethod
    def check(cls, session: Session):
        """
        Проверка параметра сортировки по цене для текущего пользователя
        """
        try:
            # TODO Почему-то не то же самое, что после записи
            check_data = session['sorted']['by_price']
            logger.error(f'Параметр сортировки: {session["sorted"]}')

            return check_data

        except KeyError:
            logger.warning('Параметры сортировки по цене не найдены')
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
            logger.warning('Параметр сортировки не найден')
            session['sorted'] = {}


    @classmethod
    def clear_data(cls, session: Session, control_parameter: str = 'None'):
        """
        Выборочная очистка ВСЕХ данных, кроме переданного параметра
        """
        logger.debug(f'Очистка параметров сортировки, кроме параметра: {control_parameter}')

        sorted_parameters = session.get('sorted', False)

        if sorted_parameters:

            for parameter in sorted_parameters.keys():
                if parameter != control_parameter:
                    try:
                        del session[parameter]
                    except KeyError:
                        logger.warning(f'Параметр сортировки {parameter} не найден')

            logger.error(f'Проверка очищенных параметров сортировки: {session["sorted"]}')

        else:
            logger.warning('Данные нельзя удалить, т.к. они еще не были записаны')


    @classmethod
    def delete(cls, session: Session):
        """
        Очистка всех параметров сортировки
        """
        try:
            session['sorted'].clear()
            logger.debug(f'Проверка параметров после очистки: { session["sorted"]}')

        except KeyError:
            logger.warning('Данные сортировки нельзя удалить, т.к. они еще не были записаны')
