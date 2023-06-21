import logging
from typing import List, Dict

from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.core.cache import cache

from config.admin import config
from ..models.products import Product
from ..forms import CommentProductForm
from ..services.products.output_products import ProductsListService
from ..services.products.detail_page import ProductCommentsService
from ..services.products.products_list.filter import ProductFilter
from ..services.products.products_list.sorting import ProductSort
from ..services.shop_cart.logic import CartProductsListService
from ..services.products.search import ProductsListSearchService
from ..services.products.browsing_history import ProductBrowsingHistoryService
from ..utils.input_data import clear_data
from ..services.products.context import SaveContextDataService


logger = logging.getLogger(__name__)


class BaseListView(ListView):
    """
    Базовое представление для вывода списка товаров (используется в ProductsListView и ProductsLisSearchView)
    """
    model = Product
    template_name = '../templates/app_shop/catalog.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        """
        Передача в шаблон параметров вывода товаров
        """
        context = super().get_context_data(**kwargs)
        context = SaveContextDataService.save_data(context=context, filter_parameters=self.filter_parameters, request=self.request)

        return context


class ProductsListView(BaseListView):
    """
    Представление для вывода каталога товаров (определенной категории, тега или всех).
    Фильтрация и сортировка по переданным в URL параметрам.
    """

    def get_queryset(self):
        """
        Вызов сервиса с бизнес-логикой для вывода товаров по переданным параметрам
        """
        logger.info(f'Новый запрос: {self.request.build_absolute_uri()}')

        # Сохраняем параметры фильтрации
        self.filter_parameters = self.kwargs | clear_data(self.request.GET)
        logger.info(f'Параметры фильтрации: {self.filter_parameters}')

        # Фильтрация по категории / тегу
        products = ProductsListService.output(filter_parameters=self.filter_parameters)

        # Фильтрация по переданным в форме параметрам
        products = ProductFilter.output(products=products, filters=self.filter_parameters)

        # Сортировка по переданным параметрам
        products = ProductSort.output(products=products, filters=self.filter_parameters)

        return products


class ProductsLisSearchView(BaseListView):
    """
    Представление для вывода найденных товаров по фразе в поисковой строке
    """

    def get_queryset(self) -> QuerySet:
        """
        Вывод товаров, найденных по поисковой фразе
        @return: список с товарами
        """
        logger.info(f'Новый запрос: {self.request.build_absolute_uri()}')

        # Сохраняем параметры фильтрации
        self.filter_parameters = self.kwargs | clear_data(self.request.GET)
        logger.info(f'Параметры фильтрации: {self.filter_parameters}')

        # Поиск товаров по названию
        products = ProductsListSearchService.search(request=self.request)

        # Фильтрация по переданным в форме параметрам
        products = ProductFilter.output(products=products, filters=self.filter_parameters)

        # Сортировка по переданным параметрам
        products = ProductSort.output(products=products, filters=self.filter_parameters)

        return products


class ProductDetailView(DetailView, FormMixin):
    """
    Представление для вывода детальной страницы товара с комментариями
    """
    model = Product
    form_class = CommentProductForm
    template_name = '../templates/app_shop/detail_product/product.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод детальной страницы товара с комментариями
        """
        id = self.kwargs["pk"]  # id товара из URL

        # Возвращаем объект из кэша / кэшируем объект
        # (кэш товара автоматически очищается в model.save() при редактировании товара)
        self.object = cache.get_or_set(f'product_{id}', self.get_object(), 60 * config.caching_time)

        context = self.get_context_data(object=self.object)
        comments = ProductCommentsService.all_comments(product=self.object)  # Комментарии к товару

        # id товаров в корзине текущего пользователя
        # (для корректного отображения кнопки добавления товара/перехода в корзину)
        cart_products = CartProductsListService.id_products(request=self.request)

        context['cart_products'] = cart_products
        context['comments'] = comments[:1]
        context['total_comments'] = comments.count()

        # Добавление записи в истории просмотра авторизованного пользователя
        if request.user.is_authenticated:
            ProductBrowsingHistoryService.save_view(request=request, product=self.object)

        return self.render_to_response(context)

    def post(self, request, pk):
        """
        Валидация и обработка данных формы с новым комментарием к товару
        """
        form = CommentProductForm(request.POST)
        product = self.get_object()
        comments = ProductCommentsService.all_comments(product=product)

        if form.is_valid():
            logger.debug(f'Данные формы валидны: {form.cleaned_data}')

            result = ProductCommentsService.add_new_comments(
                form=form,
                product=product,
                user=request.user
            )

            if result:
                return HttpResponseRedirect(reverse('shop:product_detail', kwargs={'pk': pk}))
            else:
                logger.error(f'Ошибка при публикации комментария')
                return HttpResponse('При публикации комментария произошла ошибка, попробуйте позже...')

        else:
            logger.warning(f'Невалидные данные: {form.errors}')

            return render(request, '../templates/app_shop/detail_product/product.html', context={
                'object': product,
                'comments': comments,
                'total_comments': comments.count(),
                'form': form
            })
