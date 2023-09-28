import logging

from django.db.models import QuerySet
from django.http import HttpRequest
from django.core.cache import cache

from app.config.admin import config
from app.app_shop.models.products import Product
from app.app_shop.models.cart_and_orders import Cart


logger = logging.getLogger(__name__)


class ProductsCartQuestService:
    """
    Сервис для добавления, изменения и удаления товаров в корзине неавторизованного пользователя (session)
    """

    @classmethod
    def add(cls, request: HttpRequest, product_id: str, count: int = 1) -> bool:
        """
        Метод для добавления товара в корзину пользователя (объект сессии)

        @param request: объект http-запроса
        @param product_id: id товара
        @param count: кол-во товара
        @return: bool-значение
        """
        logger.debug(
            f"Добавление товара в корзину гостя: id пользователя: "
            f"{request.user.id}, id товара - {product_id}, кол-во: {count}"
        )

        ProductsCartQuestService.check_key(
            request=request
        )  # Проверка / создание ключа "cart" в объекте сессии

        if count == 0:
            logger.warning("Нельзя добавить 0 товаров, увеличение кол-ва на 1")
            count = 1

        logger.debug(f'Корзина ДО: {request.session["cart"]}')
        record = request.session["cart"].get(product_id, False)

        if record:
            logger.warning("Товар уже есть в корзине, увеличение кол-ва")
            request.session["cart"][product_id] += count
        else:
            logger.info("Добавление нового товара")
            request.session["cart"][product_id] = count

        request.session.save()
        logger.debug(f'Корзина ПОСЛЕ: {request.session["cart"]}')

        # Очистка кэша с товарами корзины
        cls.clear_cache_cart(request=request)

        return True

    @classmethod
    def remove(cls, request: HttpRequest, product_id: int) -> None:
        """
        Метод для удаления товара из корзины (объекта сессии)

        @param request: объект http-запроса
        @param product_id: id товара
        @return: None
        """
        logger.debug(f"Удаление товара из объекта сессии: id товара - {product_id}")

        try:
            del request.session["cart"][product_id]
            request.session.save()
            logger.info("Товар удален из объекта сессии")

            # Очистка кэша с товарами корзины
            cls.clear_cache_cart(request=request)

        except KeyError:
            logger.warning(f'Не найден ключ "cart" в объекте сессии гостя')

    @classmethod
    def reduce_product(cls, request: HttpRequest, product_id: int) -> None:
        """
        Метод для уменьшения кол-ва товара на 1 (в объекте сессии)

        @param request: объект http-запроса
        @param product_id: id товара
        @return: None
        """
        logger.debug(f"Уменьшение товара на 1: id товара - {product_id}")

        product_id = str(product_id)
        count = request.session["cart"][product_id]
        count -= 1

        if count <= 0:
            logger.warning("Кол-во товара уменьшено до 0. Удаление товара из корзины")
            ProductsCartQuestService.remove(request=request, product_id=product_id)
        else:
            request.session["cart"][product_id] = count
            request.session.save()

        # Очистка кэша с товарами корзины
        cls.clear_cache_cart(request=request)

    @classmethod
    def increase_product(cls, request: HttpRequest, product_id: int) -> None:
        """
        Метод для увеличения кол-ва товара на 1 (в объекте сессии)

        @param request: объект http-запроса
        @param product_id: id товара
        @return: None
        """
        logger.debug(f"Увеличение товара на 1: id товара - {product_id}")

        product_id = str(product_id)
        count = request.session["cart"][product_id]
        count += 1

        request.session["cart"][product_id] = count
        request.session.save()

        # Очистка кэша с товарами корзины
        cls.clear_cache_cart(request=request)

    @classmethod
    def check_key(cls, request: HttpRequest) -> None:
        """
        Метод для проверки ключа в объекте сессии (создание при необходимости) для записи, чтения и удаления товаров

        @param request: объект http-запроса
        @return: None
        """
        logger.debug('Проверка ключа "cart" в объекте сессии текущего пользователя')

        if not request.session.get("cart", False):
            logger.warning("Ключ не найден, создание ключа")
            request.session["cart"] = {}

    @classmethod
    def all(cls, request: HttpRequest) -> QuerySet:
        """
        Метод для вывода всех товаров в корзине текущего пользователя (объекте сессии)

        @param request: объект http-запроса
        @return: QuerySet с товарами
        """
        logger.debug(f"Вывод товаров корзины гостя: {request.user}")

        records_list = []
        session_key = request.session.session_key
        cart_cache_key = f"cart_{session_key}"

        if cart_cache_key not in cache:
            logger.warning("В кэше для текущей сессии нет данных о товарах в корзине")
            products = request.session.get("cart", False)

            if products:
                logger.debug(f"Записи о товарах в текущей сессии гостя: {products}")

                for prod_id, count in products.items():
                    records_list.append(
                        Cart(
                            product=Product.objects.only(
                                "id", "name", "definition", "price", "discount"
                            ).get(id=prod_id),
                            count=count,
                        )
                    )

                cache.set(cart_cache_key, records_list, 60 * config.caching_time)
                logger.info("Товары сохранены в кэш")

            else:
                logger.warning("Записи о товарах не найдены")
        else:
            records_list = cache.get(cart_cache_key)

        return records_list

    @classmethod
    def clear_cache_cart(cls, request: HttpRequest) -> None:
        """
        Метод для очистки кэша с товарами в корзине

        @param request: объект http-запроса
        @return: None
        """
        logger.debug("Очистка кэша с товарами в корзине")

        session_key = request.session.session_key
        cart_cache_key = f"cart_{session_key}"

        res = cache.delete(cart_cache_key)

        if res:
            logger.info("Кэш с товарами успешно очищен")
        else:
            logger.error("Кэш с товарами не очищен")
