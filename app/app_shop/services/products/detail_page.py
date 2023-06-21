import logging

from typing import List
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from ...models.products import Product, ProductReviews
from ...forms import CommentProductForm
from app_user.models import Buyer, Profile


logger = logging.getLogger(__name__)


class ProductCommentsService:
    """
    Сервис для добавления и просмотра комментариев к товару
    """

    @classmethod
    def all_comments(cls, product = Product) -> List[ProductReviews]:
        """
        Метод для вывода всех комментариев (активных) к товару

        @param product: объект товара
        @return: список с отзывами к переданному товару
        """

        comments = ProductReviews.objects.filter(product=product, deleted=False)
        logger.debug(f'Вывод комментариев к товару: {product.name}. Комментариев: {len(comments)}')

        return comments

    @classmethod
    def add_new_comments(cls, form: CommentProductForm, product: Product, user) -> bool:
        """
        Метод для добавления нового комментария к товару
        """
        logger.debug(f'Добавление комментария к товару: {product.name}')

        input_email = form.cleaned_data["email"]
        user_email = user.email

        if input_email != user_email:
            logger.warning(f'Введенный email ({input_email}) != email пользователя ({user_email})')

        try:
           profile = Profile.objects.get(user=user)

        except ObjectDoesNotExist:
            logger.error('Профайл пользователя не найден')
            return False

        buyer, created = Buyer.objects.get_or_create(profile=profile)  # Получаем или создаем новый объект покупателя

        ProductReviews.objects.create(
            product=product,
            buyer=buyer,
            review=form.cleaned_data['review']
        )

        logger.info('Комментарий успешно опубликован')
        return True

    @classmethod
    def load_comment(cls, request: HttpRequest) -> List:
        """
        Метод для загрузки и вывода доп.комментариев к товару

        @param request: объект http-запроса
        @return: список с новыми загружаемыми комментариями и данными по ним
        """
        _LOADED_ITEM = 'loaded_item'
        _PRODUCT_ID = 'product_id'
        _LIMIT = 1

        logger.debug('Загрузка новых комментариев к товару')

        loaded_item = int(request.GET.get(_LOADED_ITEM))
        product_id = int(request.GET.get(_PRODUCT_ID))

        comments = ProductReviews.objects.filter(product=product_id)[loaded_item:loaded_item + _LIMIT]
        comments_obj = []

        for comment in comments:
            comments_obj.append({
                'avatar': comment.buyer.profile.avatar.url,
                'name': comment.buyer.profile.full_name,
                'created_at': comment.created_at,
                'review': comment.review
            })

        return comments_obj
