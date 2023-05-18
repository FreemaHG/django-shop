from django.db import models
from django.contrib.auth.models import User

from .utils.models.saving_files import save_avatar
from .utils.models.output import output_name


STATUS_CHOICES = [
    (True, 'Удалено'),
    (False, 'Активно'),
]

class Profile(models.Model):
    """
    Профайл пользователя с расширенными данными
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    phone_number = models.CharField(unique=True, max_length=10, blank=True, null=True, verbose_name='Телефон')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    avatar = models.ImageField(upload_to=save_avatar, blank=True, verbose_name='Аватар')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Учетные записи'

    def __str__(self):
        """
        Вывод имени пользователя
        """
        return output_name(self)


class Seller(models.Model):
    """
    Модель для роли продавца
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=150, verbose_name='Продавец')
    description = models.TextField(verbose_name='Описание')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление

    class Meta:
        db_table = 'seller'
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.title


class Buyer(models.Model):
    """
    Модель для роли покупателя
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    # FIXME Раскомментировать после добавления модели с товарами
    # views = models.ManyToManyField(Product, verbose_name='Просмотренные товары')
    # viewing_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время просмотра')
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')  # Мягкое удаление

    class Meta:
        db_table = 'buyer'
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        # ordering = ['-viewing_time']  # FIXME Раскомментировать после добавления модели с товарами

    def __str__(self):
        return output_name(self.profile)
