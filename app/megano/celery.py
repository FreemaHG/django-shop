import os

from celery import Celery

# Проверяем, что settings.py Django-приложения доступен через ключ DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.megano.settings")

# Инициализируем Celery, указав местоположение основной директории Celery - текущую (где celery.py)
app = Celery("app.megano")

# Определяем файл настроек Django в качестве файла конфигурации для Celery,
# предоставив пространство имен "CELERY"
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическая загрузка фоновых задач из всех зарегистрированных приложений
# Автоматический поиск в файлах tasks.py в директориях приложений, н-р, app_shop/tasks.py
app.autodiscover_tasks()
