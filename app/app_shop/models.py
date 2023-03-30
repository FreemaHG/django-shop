from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey

from .utils.models.saving_files import saving_the_category_icon, saving_the_category_image


STATUS_CHOICES = [
    (True, 'Удалено'),
    (False, 'Активно'),
]

class CategoryProduct(MPTTModel):
    """ Модель категорий товаров с вложенностью """

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, null=False, verbose_name='URL')

    icon = models.ImageField(upload_to=saving_the_category_icon, blank=True, verbose_name='Иконка')
    image = models.ImageField(upload_to=saving_the_category_image, blank=True, verbose_name='Изображение')

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
        """ Сортировка по вложенности """
        order_insertion_by = ('title',)

    class Meta:
        """ Таблица с данными, название модели в админке """
        db_table = 'categories_products'
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        """ Сохраняем URL по названию категории """
        value = self.title
        self.slug = slugify(value)  # FIXME: Должно автоматически генерировать URL ч/з prepopulated_field в админке!
        super().save(*args, **kwargs)

    def __str__(self):
        """ Возвращение названия категории """
        return self.title
