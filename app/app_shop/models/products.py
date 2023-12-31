import logging

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField
from django.core.cache import cache

from app.app_shop.utils.models.saving_files import (
    saving_the_category_icon,
    saving_the_category_image,
    saving_images_for_product,
)


logger = logging.getLogger(__name__)


STATUS_CHOICES = [
    (True, "Удалено"),
    (False, "Активно"),
]


class CategoryProduct(MPTTModel):
    """
    Модель для категорий товаров с вложенностью
    """

    title = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, null=False, verbose_name="URL")

    icon = models.ImageField(
        upload_to=saving_the_category_icon, blank=True, verbose_name="Иконка"
    )
    # Используется на главной странице для вывода категории избранных товаров
    image = models.ImageField(
        upload_to=saving_the_category_image, verbose_name="Изображение"
    )

    selected = models.BooleanField(default=False, verbose_name="Избранная категория")
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="Статус"
    )  # Мягкое удаление

    parent = TreeForeignKey(  # Вложенные категории
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """

        order_insertion_by = ("title",)

    class Meta:
        db_table = "categories_products"
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def get_absolute_url(self):
        return reverse("post-by-category", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        """
        Сохранение поля slug по названию категории
        """
        self.slug = slugify(self.title)
        super(CategoryProduct, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ProductTags(models.Model):
    """
    Модель для хранения тегов для товаров
    """

    name = models.CharField(max_length=100, verbose_name="Теги для товаров")
    slug = models.SlugField(max_length=100, blank=True, verbose_name="URL")
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="Статус"
    )  # Мягкое удаление

    class Meta:
        db_table = "product_tags"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def save(self, *args, **kwargs):
        """
        Сохранение поля slug по названию тега
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

    name = models.CharField(max_length=250, verbose_name="Название")
    definition = models.TextField(max_length=1000, verbose_name="Описание")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время добавления товара"
    )
    characteristics = JSONField(verbose_name="Характеристики")
    category = models.ForeignKey(
        CategoryProduct, on_delete=models.CASCADE, verbose_name="Категория"
    )
    tags = models.ManyToManyField("ProductTags", verbose_name="Теги")
    price = models.FloatField(
        validators=[MinValueValidator(0)], verbose_name="Стоимость"
    )
    discount = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(90)], verbose_name="Скидка (в %)"
    )
    count = models.PositiveIntegerField(default=0, verbose_name="Кол-во")
    limited_edition = models.BooleanField(
        default=False, verbose_name="Ограниченный тираж"
    )
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="Статус"
    )  # Мягкое удаление
    purchases = models.PositiveIntegerField(default=0, verbose_name="Покупок")

    class Meta:
        db_table = "products"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["id"]

    @property
    def image(self):
        return self.productimages_set.first()

    @property
    def discounted_price(self) -> int:
        """
        Расчет стоимости товара с учетом скидки
        """
        return int(self.price - ((self.price * self.discount) / 100))

    def save(self, *args, **kwargs):
        """
        Автоматическое обновление поля limited_edition в зависимости от кол-ва товара.
        Очистка кэша с данными о товаре при обновлении товара.
        """
        if 0 <= self.count <= 100:
            self.limited_edition = True
        else:
            self.limited_edition = False

        super(Product, self).save(*args, **kwargs)
        logger.info(f"Товар сохранен: id - {self.id}")

        if cache.delete(f"product_{self.id}"):
            logger.info("Кэш товара очищен")

    def __str__(self) -> str:
        return str(self.name)


class ProductBrowsingHistory(models.Model):
    """
    Модель для хранения данных об истории просмотров товаров пользователем
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    viewing_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Время просмотра"
    )

    class Meta:
        ordering = ["-viewing_time"]


class ProductImages(models.Model):
    """
    Модель для хранения изображений к товарам
    """

    title = models.CharField(max_length=250, verbose_name="Название изображения")
    image = models.ImageField(
        upload_to=saving_images_for_product, verbose_name="Изображение"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, verbose_name="Товар", related_name="images"
    )

    class Meta:
        db_table = "product_images"
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    def __str__(self) -> str:
        return str(self.title)


class ProductReviews(models.Model):
    """
    Модель для хранения отзывов о товарах
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    buyer = models.ForeignKey(
        "app_user.Buyer", on_delete=models.CASCADE, verbose_name="Покупатель"
    )
    review = models.TextField(max_length=2500, verbose_name="Отзыв")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время добавления отзыва"
    )
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="Статус"
    )  # Мягкое удаление

    class Meta:
        db_table = "products_reviews"
        verbose_name = "Отзыв о товаре"
        verbose_name_plural = "Отзывы о товаре"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.product.name
