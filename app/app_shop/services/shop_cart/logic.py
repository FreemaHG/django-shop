import logging

from typing import List
from django.db.models import QuerySet
from django.http import HttpRequest
from django.contrib.auth.models import User

from ...models.products import Product
from ...models.cart_and_orders import Cart
from .authenticated import ProductsCartUserService
from .quest import ProductsCartQuestService


logger = logging.getLogger(__name__)


class CartProductsListService:
    """
    Сервис для вывода товаров и id товаров из корзины пользователя
    (вызов нужного метода в зависимости от того, авторизован пользователь или нет)
    """

    @classmethod
    def all_products(cls, request: HttpRequest) -> QuerySet:
        """
        Метод для возврата товаров текущего пользователя: из БД для авторизованного / из объекта сессии для гостя

        @param request: объект http-запроса
        @return: QuerySet с товарами
        """
        logger.debug("Возврат товаров текущего пользователя")
        user = request.user

        if user.is_authenticated:
            logger.debug("Пользователь авторизован")
            products = ProductsCartUserService.all(user=user)

        else:
            logger.debug("Пользователь НЕ авторизован")
            products = ProductsCartQuestService.all(request=request)

        return products

    @classmethod
    def id_products(cls, request: HttpRequest) -> List[int]:
        """
        Метод для возврата списка с id товаров текущего пользователя

        @param request: объект http-запроса
        @return: список с id товаров
        """
        logger.debug("Получение списка id товаров в корзине текущего пользователя")

        id_list = []

        if request.user.is_authenticated:
            logger.debug("Пользователь авторизован")

            products = CartProductsListService.all_products(request=request)

            for record in products:
                id_list.append(record.product.id)

        else:
            logger.debug("Пользователь не авторизован")
            records = request.session.get("cart", False)

            if records:
                logger.debug("В объекте сессии имеются данные о товарах")
                id_list = list(map(int, records.keys()))

        logger.info(f"Список с id товаров: {id_list}")

        return id_list


class CartProductsService:
    """
    Сервис для добавления, удаления и проверки товара в корзине.
    Вызов методов в зависимости от того, авторизован пользователь или нет.
    """

    @classmethod
    def add(cls, request: HttpRequest, product_id: int = None, count: int = 1) -> bool:
        """
        Метод для добавления товара в корзину

        @param request: объект http-запроса
        @param product_id: id товара
        @param count: кол-во товара
        @return: True / False в зависимости от результата
        """
        logger.debug("Добавление товара в корзину")

        if not product_id:
            logger.warning(
                "id товара не передан в качестве аргумента функции, поиск данных в URL"
            )
            product_id = int(request.GET.get("product_id"))
            count = int(request.GET.get("count", 1))

        logger.debug(f"id товара: {product_id}, кол-во: {count}")

        if request.user.is_authenticated:
            # Добавление товара в корзину зарегистрированного пользователя
            res = ProductsCartUserService.add(
                user=request.user, product_id=product_id, count=count
            )

        else:
            # Добавление товара в корзину гостя (запись в объект сессии)
            res = ProductsCartQuestService.add(
                request=request, product_id=str(product_id), count=count
            )

        return res

    @classmethod
    def check_cart(cls, request: HttpRequest, product_id: int) -> bool:
        """
        Метод для проверки товара в корзине пользователя

        @param request: объект http-запроса
        @param product_id: id товара
        @return: True / False в зависимости от проверки
        """
        logger.debug("Проверка товара в корзине пользователя")

        res = ProductsCartUserService.check_product(
            user=request.user, product_id=product_id
        )
        return res

    @classmethod
    def reduce_product(cls, request: HttpRequest, product_id: int) -> None:
        """
        Метод для уменьшения кол-ва товара в корзине

        @param request: объект http-запроса
        @param product_id: id товара
        @return: None
        """
        if request.user.is_authenticated:
            logger.debug("Пользователь авторизован")
            ProductsCartUserService.reduce_product(
                user=request.user, product_id=product_id
            )
        else:
            logger.debug("Пользователь НЕ авторизован")
            ProductsCartQuestService.reduce_product(
                request=request, product_id=product_id
            )

    @classmethod
    def increase_product(cls, request: HttpRequest, product_id: int) -> None:
        """
        Метод для увеличения кол-ва товара в корзине

        @param request:
        @param product_id: id товара
        @return: None
        """
        if request.user.is_authenticated:
            logger.debug("Пользователь авторизован")
            ProductsCartUserService.increase_product(
                user=request.user, product_id=product_id
            )
        else:
            logger.debug("Пользователь НЕ авторизован")
            ProductsCartQuestService.increase_product(
                request=request, product_id=product_id
            )

    @classmethod
    def delete(cls, request: HttpRequest, product_id: int) -> None:
        """
        Метод для удаления товара из корзины

        @param request: объект http-запроса
        @param product_id: id товара
        @return: None
        """
        if request.user.is_authenticated:
            # Удаление товара из корзины зарегистрированного пользователя
            ProductsCartUserService.remove(user=request.user, product_id=product_id)
        else:
            # Удаление товара из корзины гостя (объект сессии)
            ProductsCartQuestService.remove(request=request, product_id=product_id)

    @classmethod
    def merge_carts(cls, request: HttpRequest, user: User) -> None:
        """
        Метод для слияния корзин (если есть записи) при регистрации и авторизации

        @param request: объект http-запроса
        @param user: объект пользователя
        @return: None
        """
        logger.debug("Слияние корзин при регистрации/авторизации пользователя")

        records = request.session.get("cart", False)
        new_records = []

        if records:
            logger.debug(f"Имеются данные для слияния: {records}")

            for prod_id, count in records.items():
                logger.debug(f"Поиск товара в БД по id - {prod_id}")
                product = Product.objects.get(id=prod_id)
                logger.debug(f"Товар найден: {product.name}")

                # Проверка, есть ли товар уже в корзине зарегистрированного пользователя
                deferred_product = Cart.objects.filter(
                    user=user, product=product
                ).first()

                if deferred_product:
                    logger.warning(
                        f"Товар уже есть в корзине: id - {deferred_product.id}, "
                        f"{deferred_product.count} шт., суммирование кол-ва"
                    )

                    deferred_product.count += count  # Суммируем кол-во товара
                    deferred_product.save(update_fields=["count"])

                else:
                    logger.info(
                        f"Добавление нового товара: {product.name}, {count} шт."
                    )

                    new_records.append(
                        Cart(
                            user=user,
                            product=Product.objects.get(id=prod_id),
                            count=count,
                        )
                    )

            Cart.objects.bulk_create(new_records)
            logger.info("Данные успешно записаны в БД")

            del request.session["cart"]  # Удаляем записи из сессии
            request.session.save()
            logger.info("Объект сессии успешно очищен")

        else:
            logger.warning("Нет записей для слияния")
