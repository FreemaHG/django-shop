import os.path


IMAGES_PATH = os.path.join('images', 'logo')

def saving_logo(instance, filename: str) -> str:
    """
    Сохранение логотипа сайта
    """
    return os.path.join(IMAGES_PATH, filename)
