import logging

from typing import List
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from ...models import Product, ProductReviews
from app_user.models import Buyer, Profile
from ...forms import CommentProductForm


logger = logging.getLogger(__name__)

class DetailProduct:
    """
    Сервисы, используемые при просмотре детальной страницы товара
    """

    @classmethod
    def add_item_to_viewed(cls):
        """ Добавление товара в список просмотренных текущим пользователем """
        ...

    @classmethod
    def all_comments(cls, product = Product) -> List[ProductReviews]:
        """ Вывод всех комментариев к товару """
        comments = ProductReviews.objects.filter(product=product, deleted=False)
        logger.debug(f'Вывод всех активных комментариев к товару: {product.name}. Найдено комментариев: {len(comments)}')

        return comments

    @classmethod
    def add_new_comments(cls, form: CommentProductForm, product: Product, user) -> bool:
        """ Добавить новый комментарий к товару """

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
