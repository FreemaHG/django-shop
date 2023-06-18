import logging

from typing import Dict
from django.http import HttpRequest

from ...services.shop_cart.logic import CartProductsListService


logger = logging.getLogger(__name__)


class SaveContextDataService:
    """
    Сервис для сохранения данных в контексте представления.
    Используется для сохранения параметров поиска, фильтрации и сортировки для последующего вывода в шаблоне.
    """

    _CLASS_UP = 'Sort-sortBy_dec'
    _CLASS_DOWN = 'Sort-sortBy_inc'

    @classmethod
    def save_data(cls, context: Dict, filter_parameters: Dict, request: HttpRequest) -> Dict:
        """
        Метод для сохранения данных в контексте представления

        @param request:
        @param filter_parameters: словарь с данными для сохранения
        @param context: словарь с контекстными данными из представления
        @return: словарь с обновленными контекстными данными из представления
        """

        context = cls.save_products_id(context=context, request=request)

        if filter_parameters:
            context = cls.save_filter_param(context=context, filter_parameters=filter_parameters)

            # Передача в шаблон индикатора сортировки
            sort_param = filter_parameters.get('sort', False)

            if not sort_param is False:
               context = cls.save_sorting_param(context=context, sort_param=sort_param)

            query = request.GET.get('query', False)

            if query:
                context = cls.save_query(context=context, query=query)

            logger.warning(f'Передача параметров в шаблон: {context["filter_parameters"]}')

        logger.warning('Параметры фильтрации не заданы')

        return context

    @classmethod
    def save_query(cls, context: Dict, query: str):
        logger.debug(f'Сохранение поисковой фразы в контексте: {query}')
        context['query'] = query

        return context

    @classmethod
    def save_products_id(cls, context: Dict, request: HttpRequest):
        context['products_id'] = CartProductsListService.id_products(request=request)  # id товаров в корзине текущего пользователя

        return context

    @classmethod
    def save_filter_param(cls, context: Dict, filter_parameters: Dict):
        # Передача в шаблон параметров фильтрации
        context['filter_parameters'] = filter_parameters

        return context

    @classmethod
    def save_sorting_param(cls, context: Dict, sort_param: Dict):
        context['filter_parameters']['sort'] = sort_param

        # Сортировка по цене
        if sort_param == 'by_price_down':
            context['sorting_indicator_by_price'] = cls._CLASS_UP  # Сортировка вверх

        elif sort_param == 'by_price_up':
            context['sorting_indicator_by_price'] = cls._CLASS_DOWN  # Сортировка вниз

        # Сортировка по популярности (кол-ву продаж)
        elif sort_param == 'by_popularity_down':
            context['sorting_indicator_by_popularity'] = cls._CLASS_UP

        elif sort_param == 'by_popularity_up':
            context['sorting_indicator_by_popularity'] = cls._CLASS_DOWN

        # Сортировка по отзывам
        elif sort_param == 'by_reviews_down':
            context['sorting_indicator_by_reviews'] = cls._CLASS_UP

        elif sort_param == 'by_reviews_up':
            context['sorting_indicator_by_reviews'] = cls._CLASS_DOWN

        # Сортировка по новизне
        elif sort_param == 'by_novelty_down':
            context['sorting_indicator_by_novelty'] = cls._CLASS_UP

        elif sort_param == 'by_novelty_up':
            context['sorting_indicator_by_novelty'] = cls._CLASS_DOWN

        return context
