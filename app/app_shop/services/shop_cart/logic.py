import logging

from typing import List
from django.db.models import Sum
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ...models import Cart, Product
from .authenticated import ProductsCartUserService
from .quest import ProductsCartQuestService


logger = logging.getLogger(__name__)


class CartProductsListService:

    # FIXME Переименовать в all_products
    @classmethod
    def output(cls, request: HttpRequest):
        """
        Возврат товаров текущего пользователя: из БД для авторизованного / из объекта сессии для гостя
        """
        logger.debug('Возврат товаров текущего пользователя')
        user = request.user

        if user.is_authenticated:
            logger.info('Пользователь авторизован')
            products = ProductsCartUserService.all(user=user)
        else:
            logger.info('Пользователь НЕ авторизован')
            products = ProductsCartQuestService.all(request=request)

        return products

    @classmethod
    def id_products(cls, request: HttpRequest):
        """
        Возврат списка с id товаров текущего пользователя
        """
        logger.debug('Получение списка id товаров в корзине текущего пользователя')

        id_list = []

        if request.user.is_authenticated:
            logger.debug('Пользователь авторизован')
            products = CartProductsListService.output(request=request)

            # FIXME Сделать умнее!
            for record in products:
                id_list.append(record.product.id)

        else:
            logger.debug('Пользователь не авторизован')
            records = request.session.get('cart', False)

            if records:
                logger.debug('В объекте сессии имеются данные о товарах')
                id_list = list(map(int, records.keys()))

        logger.info(f'Список с id товаров: {id_list}')

        return id_list


# FIXME Переименовать в CartProductsService
class CartProductsAddService:
    """
    Добавление, удаление проверка товара в корзине.
    Вызов методов в зависимости от того, авторизован пользователь или нет.
    """

    @classmethod
    def add(cls, request: HttpRequest, product_id: int = None, count: int = 1):
        """
        Добавление товара в корзину
        """
        if not product_id:
            logger.warning('id товара не передан в качестве аргумента функции')
            product_id = int(request.GET.get('product_id'))
            count = int(request.GET.get('count', 1))

        logger.info(f'id товара: {product_id}, кол-во: {count}')

        if request.user.is_authenticated:
            # Добавление товара в корзину зарегистрированного пользователя
            res = ProductsCartUserService.add(user=request.user, product_id=product_id, count=count)
        else:
            # Добавление товара в корзину гостя (запись в объект сессии)
            res = ProductsCartQuestService.add(request=request, product_id=str(product_id), count=count)

        return res

    # FIXME Возможно метод не нужен, перепроверить!
    @classmethod
    def check_cart(cls, request: HttpRequest, product_id: int):
        """
        Проверка товара в корзине пользователя
        """
        logger.debug('Проверка товара в корзине пользователя')

        if request.user.is_authenticated:
            logger.debug('Пользователь авторизован')
            res = ProductsCartUserService.check_product(user=request.user, product_id=product_id)
        else:
            logger.debug('Пользователь НЕ авторизован')
            res = ProductsCartQuestService.check_product(request=request, product_id=product_id)

        return res


    @classmethod
    def reduce_product(cls, request: HttpRequest, product_id: int):
        """
        Уменьшение кол-ва товара в корзине
        """
        if request.user.is_authenticated:
            logger.debug('Пользователь авторизован')
            ProductsCartUserService.reduce_product(user=request.user, product_id=product_id)
        else:
            logger.debug('Пользователь НЕ авторизован')
            ProductsCartQuestService.reduce_product(request=request, product_id=product_id)


    @classmethod
    def increase_product(cls, request: HttpRequest, product_id: int):
        """
        Уменьшение кол-ва товара в корзине
        """
        if request.user.is_authenticated:
            logger.debug('Пользователь авторизован')
            ProductsCartUserService.increase_product(user=request.user, product_id=product_id)
        else:
            logger.debug('Пользователь НЕ авторизован')
            ProductsCartQuestService.increase_product(request=request, product_id=product_id)


    @classmethod
    def delete(cls, request: HttpRequest, product_id: int):
        """
        Удаление товара из корзины
        """
        # FIXME НУжен ли res?
        if request.user.is_authenticated:
            # Удаление товара из корзины зарегистрированного пользователя
            res = ProductsCartUserService.remove(user=request.user, product_id=product_id)
        else:
            # Удаление товара из корзины гостя (объект сессии)
            res = ProductsCartQuestService.remove(request=request, product_id=product_id)

        return res

    @classmethod
    def merge_carts(cls, request: HttpRequest, user=User):
        """
        Слияние корзин (если есть записи) при регистрации и авторизации
        """
        logger.debug('Слияние корзин при регистрации/авторизации пользователя')
        records = request.session.get('cart', False)
        new_records = []

        if records:
            logger.debug(f'Имеются данные для слияния: {records}')
            for prod_id, count in records.items():
                # FIXME Оптимизировать
                logger.debug(f'Поиск товара в БД по id - {prod_id}')
                product = Product.objects.get(id=prod_id)
                logger.debug(f'Товар найден: {product.name}')

                # Проверка, есть ли товар уже в корзине зарегистрированного пользователя
                deferred_product = Cart.objects.filter(user=user, product=product).first()

                if deferred_product:
                    logger.warning(f'Товар уже есть в корзине: id - {deferred_product.id}, {deferred_product.count} шт., суммирование кол-ва')
                    deferred_product.count += count  # Суммируем кол-во товара
                    deferred_product.save()

                else:
                    logger.info(f'Добавление нового товара: {product.name}, {count} шт.')
                    new_records.append(Cart(
                        user=user,
                        product=Product.objects.get(id=prod_id),
                        count=count
                    ))

            Cart.objects.bulk_create(new_records)
            logger.info('Данные успешно записаны в БД')

            del request.session['cart']  # Удаляем записи из сессии
            request.session.save()
            logger.info('Объект сессии успешно очищен')

        else:
            logger.warning('Нет записей для слияния')
