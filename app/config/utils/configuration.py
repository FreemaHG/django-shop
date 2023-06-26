from ..models import SiteConfiguration


def get_config() -> SiteConfiguration:
    """
    Функция для получения основных настроек сайта из модели SiteConfiguration
    """
    try:
        # Получаем один имеющийся элемент из БД
        config = SiteConfiguration.objects.get()

    except:
        # Создаем элемент, если он не существует
        config = SiteConfiguration.get_solo()

    return config
