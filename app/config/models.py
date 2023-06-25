import logging

from django.core.validators import MaxValueValidator
from django.db import models
from solo.models import SingletonModel
from functools import lru_cache

from .utils.saving_fales import saving_logo
from app_shop.models.products import CategoryProduct


logger = logging.getLogger(__name__)

class SiteConfiguration(SingletonModel):
    """
    Ключевые настройки сайта
    """
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')
    site_url = models.URLField(max_length=150, null=True, verbose_name='URL')
    logo_head = models.ImageField(upload_to=saving_logo, verbose_name='Логотип в шапке')
    logo_footer = models.ImageField(upload_to=saving_logo, verbose_name='Логотип в футере')

    # Для вывода избранных категорий товаров на главной
    selected_products = models.ManyToManyField(CategoryProduct, verbose_name='Избранные товары')

    # Стоимость доставки
    shipping_cost = models.IntegerField(default=200, verbose_name='Стоимость обычной доставки (руб.)')
    extra_shipping_cost = models.IntegerField(default=500,
                                              verbose_name='Надбавочная стоимость для экспресс-доставки (руб.)')
    min_order_cost = models.IntegerField(default=2000,
                                         verbose_name='Минимальная стоимость заказа для бесплатной доставки (руб.)')

    caching_time = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(168)], verbose_name='Кэширование (кол-во часов)')
    maintenance_mode = models.BooleanField(default=False, verbose_name='Режим обслуживания')

    def __str__(self):
        return 'Конфигурация сайта'

    @classmethod
    @lru_cache(maxsize=1)  # Кэширование модели при первом запросе
    def get_solo(cls):
        """
        Создание объекта
        """
        return super().get_solo()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.get_solo.cache_clear()  # Очистка кэша при внесении изменений

    class Meta:
        verbose_name = 'Конфигурация сайта'
