from app.megano.celery import app as celery_app

# Чтобы убедиться, что приложение Celery загружается при запуске Django, явно импортируем его в __all__:
__all__ = ("celery_app",)
