import logging

from typing import List, Dict
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpRequest

# from config.admin import config
from app.config.utils.configuration import get_config
from app.app_user.models import Buyer, Profile
from app.app_shop.models.products import Product, ProductReviews
from app.app_shop.forms import CommentProductForm


logger = logging.getLogger(__name__)


class ProductCommentsService:
    """
    Сервис для добавления и просмотра комментариев к товару
    """

    @classmethod
    def all_comments(cls, product: Product = None, product_id: int = None) -> QuerySet:
        """
        Метод для вывода всех (активных) комментариев к товару

        @param product_id: id товара (не обязательный параметр)
        @param product: объект товара (не обязательный параметр)
        @return: список с отзывами для указанного товара
        """
        logger.debug("Вывод комментариев к товару")

        config = get_config()

        if product_id:
            comments = cache.get_or_set(
                f"comments_product_{product_id}",
                ProductReviews.objects.select_related(
                    "buyer__profile", "buyer__profile__user"
                )
                .only(
                    "created_at",
                    "review",
                    "buyer__profile__full_name",
                    "buyer__profile__avatar",
                    "buyer__profile__user__id",
                )
                .filter(product__id=product_id, deleted=False),
                60 * config.caching_time,
            )
        else:
            comments = cache.get_or_set(
                f"comments_product_{product.id}",
                ProductReviews.objects.select_related("buyer").filter(
                    product=product, deleted=False
                ),
                60 * config.caching_time,
            )

        logger.debug(f"Кол-во комментариев: {len(comments)}")

        return comments

    @classmethod
    def add_new_comments(
        cls, form: CommentProductForm, product: Product, user: User
    ) -> bool:
        """
        Метод для добавления нового комментария к товару

        @param form: объект формы с данными для добавления нового комментария
        @param product: объект товара, к которому оставляется комментарий
        @param user: текущий пользователь
        @return: True / False в зависимости от успешности
        """
        logger.debug(f"Добавление комментария к товару: {product.name}")

        input_email = form.cleaned_data["email"]
        user_email = user.email

        if input_email != user_email:
            logger.warning(
                f"Введенный email ({input_email}) != email пользователя ({user_email})"
            )

        try:
            profile = Profile.objects.get(user=user)
            logger.debug("Профайл пользователя найден")

        except ObjectDoesNotExist:
            logger.error("Профайл пользователя не найден")
            return False

        buyer, created = Buyer.objects.get_or_create(
            profile=profile
        )  # Получаем или создаем новый объект покупателя

        ProductReviews.objects.create(
            product=product, buyer=buyer, review=form.cleaned_data["review"]
        )

        # Очистка кэша с комментариями к текущему товару
        cache.delete(f"comments_product_{product.id}")

        logger.info("Комментарий успешно создан")
        return True

    @classmethod
    def load_comment(cls, request: HttpRequest) -> List[Dict]:
        """
        Метод для загрузки и вывода доп.комментариев к товару

        @param request: объект http-запроса
        @return: список с новыми загружаемыми комментариями и данными по ним
        """
        logger.debug("Загрузка новых комментариев к товару")

        _LOADED_ITEM = "loaded_item"
        _PRODUCT_ID = "product_id"
        _LIMIT = 1

        loaded_item = int(request.GET.get(_LOADED_ITEM))
        product_id = int(request.GET.get(_PRODUCT_ID))

        comments = cls.all_comments(product_id=product_id)[
            loaded_item : loaded_item + _LIMIT
        ]
        comments_obj = []

        for comment in comments:
            comments_obj.append(
                {
                    "avatar": comment.buyer.profile.avatar.url,
                    "name": comment.buyer.profile.full_name,
                    "created_at": comment.created_at,
                    "review": comment.review,
                }
            )

        return comments_obj
