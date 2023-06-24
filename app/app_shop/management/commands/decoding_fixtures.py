import json
import os.path

from django.core.management.base import BaseCommand
from django.conf import settings


PATH = os.path.join(settings.BASE_DIR, 'fixtures')  # Директория с фикстурами

class Command(BaseCommand):
    """
    Команда для перекодирования файла с фикстурами для последующего импорта в БД
    """
    def handle(self, *args, **options) -> None:
        with open(os.path.join(PATH, 'db.json'), encoding='windows-1251') as f:  # Открываем старый файл с фикстурами
            data = json.load(f)  # Подгружаем json-данные
        with open(os.path.join(PATH, 'encoding-db.json'), 'w', encoding='utf-8') as f:  # Создаем новый файл
            json.dump(data, f, ensure_ascii=False)  # ensure_ascii=False - отключает экранирование не-ASCII символов!
