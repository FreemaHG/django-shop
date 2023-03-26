import os.path


IMAGES_PATH = os.path.join('images', 'categories')

def saving_the_category_icon(instance, filename: str) -> str:
    """ Сохранение иконки категории товаров """
    return os.path.join(IMAGES_PATH, 'icons', f'{instance.title}', f'{filename}')


def saving_the_category_image(instance, filename: str) -> str:
    """ Сохранение изображения категории товаров """
    return os.path.join(IMAGES_PATH, 'images', f'{instance.title}', f'{filename}')
