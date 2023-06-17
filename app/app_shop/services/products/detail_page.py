import logging

from typing import List
from django.core.exceptions import ObjectDoesNotExist

from ...models import Product, ProductReviews
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

        logger.debug(f'Публикация комментария к статье: {product.name}')

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
