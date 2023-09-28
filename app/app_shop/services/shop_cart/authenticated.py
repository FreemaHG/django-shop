import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db.models import QuerySet

from app.config.admin import config
from app.app_shop.models.products import Product
from app.app_shop.models.cart_and_orders import Cart


logger = logging.getLogger(__name__)


class ProductsCartUserService:
    """
    Сервис для добавления, изменения и удаления товаров в корзине авторизованного пользователя (БД)
    """

    @classmethod
    def add(cls, user: User, product_id: int, count: int = 1) -> bool:
        """
        Метод для добавления товара в корзину пользователя

        @param user: объект пользователя
        @param product_id: id товара
        @param count: кол-во добавляемого товара
        @return:
        """
        logger.debug(
            f"Добавление товара в корзину: user - {user.id}, id товара - {product_id}, кол-во: {count}"
        )

        try:
            product = Product.objects.get(id=product_id)
            logger.info(f"Товар найден: {product.name}")

        except ObjectDoesNotExist:
            logger.error("Товар не найден")
            return False

        if count == 0:
            logger.warning(
                "Нельзя добавить 0 товаров в корзину, увеличение кол-ва на 1"
            )
            count = 1

        if ProductsCartUserService.check_product(user=user, product_id=product_id):
            logger.warning("Добавляемый товар уже есть в корзине пользователя")
            ProductsCartUserService.change_quantity(
                user=user, product_id=product_id, count=count
            )
        else:
            Cart.objects.create(user=user, product=product, count=count)

        # Очистка кэша с товарами в корзине пользователя
        cache.delete(f"cart_{user.id}")

        return True

    @classmethod
    def remove(cls, user: User, product_id: int) -> None:
        """
        Метод для удаления товара из корзины

        @param user: объект пользователя
        @param product_id: id товара
        @return: None
        """
        logger.debug(f"Удаление товара из корзины: user - {user.id}, id - {product_id}")

        Cart.objects.filter(user=user, product__id=product_id).delete()

        # Очистка кэша с товарами в корзине пользователя
        cache.delete(f"cart_{user.id}")

    @classmethod
    def change_quantity(cls, user: User, product_id: int, count: int) -> None:
        """
        Метод для изменения кол-во товара в корзине пользователя

        @param user: объект пользователя
        @param product_id: id товара
        @param count: кол-во товара (может быть > 0 / < 0)
        @return: None
        """
        logger.debug(
            f"Изменение кол-ва товара в корзине: пользователь - {user.id}, id товара - {product_id}, изменить на - {count}"
        )

        record = Cart.objects.get(user=user, product__id=product_id)
        record.count += count

        if record.count <= 0:
            logger.warning(
                "Кол-во товара меньше или равно 0. Удаление товара из корзины"
            )
            ProductsCartUserService.remove(user=user, product_id=product_id)

        else:
            record.save(update_fields=["count"])
            logger.info(f"Товар: id - {product_id}, кол-во: {record.count}")

        # Очистка кэша с товарами в корзине пользователя
        cache.delete(f"cart_{user.id}")

    @classmethod
    def reduce_product(cls, user: User, product_id: int) -> None:
        """
        Метод для уменьшения кол-ва товара на 1

        @param user: объект пользователя
        @param product_id: id товара
        @return: None
        """
        logger.debug(
            f"Уменьшение товара в корзине пользователя на 1: id товара - {product_id}"
        )

        record = Cart.objects.get(user=user, product__id=product_id)
        record.count -= 1

        if record.count > 0:
            record.save(update_fields=["count"])

        else:
            logger.warning("Кол-во товара уменьшено до 0. Удаление товара из корзины")
            ProductsCartUserService.remove(user=user, product_id=product_id)

        # Очистка кэша с товарами в корзине пользователя
        cache.delete(f"cart_{user.id}")

    @classmethod
    def increase_product(cls, user: User, product_id: int) -> None:
        """
        Метод для увеличения кол-ва товара на 1

        @param user: объект пользователя
        @param product_id: id товара
        @return: None
        """
        logger.debug(
            f"Увеличение товара в корзине пользователя на 1: id товара - {product_id}"
        )

        record = Cart.objects.get(user=user, product__id=product_id)
        record.count += 1
        record.save(update_fields=["count"])

        # Очистка кэша с товарами в корзине пользователя
        cache.delete(f"cart_{user.id}")

    @classmethod
    def check_product(cls, user: User, product_id: int) -> bool:
        """
        Метод для проверки, есть ли указанный товар в корзине текущего пользователя

        @param user: объект пользователя
        @param product_id: id товара
        @return: True / False в зависимости от проверки
        """
        logger.debug("Проверка товара в корзине текущего пользователя")

        try:
            Cart.objects.get(user=user, product__id=product_id)
            logger.debug("Товар есть в корзине")
            return True

        except ObjectDoesNotExist:
            logger.debug("Товара нет в корзине")
            return False

    @classmethod
    def all(cls, user: User) -> QuerySet:
        """
        Метод для вывода всех товаров в корзине текущего пользователя

        @param user: объект пользователя
        @return: QuerySet с товарами в корзине пользователя
        """
        logger.debug(f"Вывод товаров из корзины покупателя")

        products = cache.get_or_set(
            f"cart_{user.id}",
            Cart.objects.select_related("product")
            .only(
                "id",
                "count",
                "product__id",
                "product__name",
                "product__definition",
                "product__price",
                "product__discount",
            )
            .filter(user=user),
            60 * config.caching_time,
        )

        return products

    @classmethod
    def total_cost(cls, products: QuerySet) -> int:
        """
        Метод для возврата общей стоимости товаров в корзине пользователя

        @param products: QuerySet с товарами
        @return: число - общая стоимость товаров
        """
        logger.debug("Подсчет общей стоимости товаров в корзине")

        total_cost = sum(product.position_cost for product in products)
        return total_cost

    @classmethod
    def clear_cart(cls, user: User) -> None:
        """
        Метод для очистки корзины (после успешного оформления заказа)

        @param user: объект пользователя
        @return: None
        """
        logger.debug("Запуск сервиса по очистке корзины")

        Cart.objects.filter(user=user).delete()
        cache.delete(f"cart_{user.id}")
