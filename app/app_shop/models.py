import logging

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum, F
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField
from django.core.cache import cache

from .utils.models.saving_files import (
    saving_the_category_icon,
    saving_the_category_image,
    saving_images_for_product
)


logger = logging.getLogger(__name__)

STATUS_CHOICES = [
    (True, 'Удалено'),
    (False, 'Активно'),
]

class CategoryProduct(MPTTModel):
    """
    Модель категорий товаров с вложенностью
    """
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, null=False, verbose_name='URL')

    icon = models.ImageField(upload_to=saving_the_category_icon, blank=True, verbose_name='Иконка')
    # Используется на главной странице для вывода категории избранных товаров
    image = models.ImageField(upload_to=saving_the_category_image, verbose_name='Изображение')

    selected = models.BooleanField(default=False, verbose_name='Избранная категория')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление

    parent = TreeForeignKey(  # Вложенные категории
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        db_table = 'categories_products'
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    # TODO точно нужно?
    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        """
        Сохраняем URL по названию категории
        """
        self.slug = slugify(self.title)
        super(CategoryProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductTags(models.Model):
    """
    Модель для хранения тегов для товаров
    """
    name = models.CharField(max_length=100, verbose_name='Теги для товаров')
    slug = models.SlugField(max_length=100, blank=True, verbose_name='URL')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление

    class Meta:
        db_table = 'product_tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def save(self, *args, **kwargs):
        """
        Сохраняем URL по названию тега
        """
        if not self.slug:
            self.slug = slugify(self.name)

        super(ProductTags, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель для хранения данных о товаре
    """
    name = models.CharField(max_length=250, verbose_name='Название')
    definition = models.TextField(max_length=1000, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления товара')
    characteristics = JSONField(verbose_name='Характеристики')
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField('ProductTags', verbose_name='Теги')
    price = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Стоимость')
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(90)], verbose_name='Скидка (в %)')
    count = models.PositiveIntegerField(default=0, verbose_name='Кол-во')
    limited_edition = models.BooleanField(default=False, verbose_name='Ограниченный тираж')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление
    purchases = models.PositiveIntegerField(default=0, verbose_name='Покупок')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']

    @property
    def discounted_price(self):
        """
        Цена товара с учетом скидки
        """
        return int(self.price - ((self.price * self.discount) / 100))

    def save(self, *args, **kwargs):
        """
        Меняем поле limited_edition в зависимости от кол-ва товара
        """
        if 0 <= self.count <= 100:
            self.limited_edition = True
        else:
            self.limited_edition = False

        super(Product, self).save(*args, **kwargs)
        logger.info(f'Товар сохранен: id - {self.id}')

        if cache.delete(f"product_{self.id}"):
            logger.info('Кэш товара очищен')


    def __str__(self):
        return self.name


class ProductBrowsingHistory(models.Model):
    """
    История просмотров товаров пользователя
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    viewing_time = models.DateTimeField(auto_now_add=True, verbose_name='Время просмотра')

    class Meta:
        ordering = ['-viewing_time']


class ProductImages(models.Model):
    """
    Модель для хранения изображений к товарам
    """
    title = models.CharField(max_length=250, verbose_name='Название изображения')
    image = models.ImageField(upload_to=saving_images_for_product, verbose_name='Изображение')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'

    def __str__(self):
        return self.title


class ProductReviews(models.Model):
    """
    Модель для хранения отзывов о товарах
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    buyer = models.ForeignKey('app_user.Buyer', on_delete=models.CASCADE, verbose_name='Покупатель')
    # # TODO Точно нужно?
    # rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=2500, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления отзыва')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление

    class Meta:
        db_table = 'products_reviews'
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товаре'
        ordering = ['created_at']

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    """
    Корзина с товарами
    """
    # null=True нужно исключительно для создания экземпляра корзины для анонимного пользователя из данных сессии
    # с последующей передачей данных в шаблон, чтобы не делать новую верстку под корзину неавторизованного пользователя
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.PositiveIntegerField(default=1, verbose_name='Кол-во')

    class Meta:
        db_table = 'products_cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'Корзина покупателя'

        # if not self.user is None and self.user.profile:
        #     return f'Корзина покупателя: {self.user.profile.full_name}'
        # else:
        #     return 'Корзина гостя'

        # try:
        #     return f'Корзина покупателя: {self.user.profile.full_name}'
        # except self.RelatedObjectDoesNotExist:
        #     return 'Корзина гостя'

    @property
    def position_cost(self):
        """
        Стоимость одной позиции товара с учетом скидки и кол-ва товара (с округлением до целого)
        """
        product = self.product
        price = product.price

        return int((price - (price * (product.discount / 100))) * self.count)


class PaymentErrors(models.Model):
    """
    Сообщения ошибок при оплате заказа
    """
    title = models.CharField(max_length=150, verbose_name='Сообщение ошибки')
    description = models.CharField(max_length=500, verbose_name='Описание ошибки')

    class Meta:
        db_table = 'payment_errors'
        verbose_name = 'Ошибка оплаты'
        verbose_name_plural = 'Ошибки оплаты'

    def __str__(self):
        return self.title


class Order(models.Model):
    """
    Заказ
    """
    STATUS_CHOICES = (
        (1, 'Оформлен'),
        (2, 'Не оплачен'),
        (3, 'Подтверждение оплаты'),
        (4, 'Оплачен'),
        (5, 'Доставляется'),
    )

    DELIVERY_CHOICES = (
        (1, 'Обычная доставка'),
        (2, 'Экспресс доставка'),
    )

    PAYMENT_CHOICES = (
        (1, 'Онлайн картой'),
        (2, 'Онлайн со случайного чужого счета'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    city = models.CharField(max_length=100, null=True, verbose_name='Город')
    address = models.CharField(max_length=500, null=True, verbose_name='Адрес доставки')

    # TODO Возможно переделать в отдельные таблицы с выводом в шаблоне вариантов из БД
    delivery = models.IntegerField(choices=DELIVERY_CHOICES, default=1, verbose_name='Тип доставки')
    payment = models.IntegerField(choices=PAYMENT_CHOICES, default=1, verbose_name='Оплата')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='Статус')
    error_message = models.ForeignKey(PaymentErrors, on_delete=models.SET_NULL, null=True, verbose_name='Сообщение об ошибке')

    @property
    def order_cost(self):
        """
        Стоимость заказа
        """
        # FIXME Оптимизировать в одну строку
        products = PurchasedProduct.objects.filter(order__id=self.id)
        amount = products.aggregate(amount=Sum(F('count') * F('price')))

        return amount['amount']

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-data_created']

    def __str__(self):
        return f'Заказ №{self.id}'


class PurchasedProduct(models.Model):
    """
    Купленные товары
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Наименование товара')
    count = models.PositiveIntegerField(verbose_name='Кол-во')
    price = models.PositiveIntegerField(verbose_name='Цена')  # Берется из корзины с учетом скидки!

    class Meta:
        db_table = 'purchased_products'
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return self.product.name

    @property
    def position_cost(self):
        """
        Стоимость одной позиции товара с кол-ва (с округлением до целого)
        """
        return int(self.price * self.count)
