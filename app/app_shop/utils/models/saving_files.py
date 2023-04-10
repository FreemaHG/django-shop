import os.path


IMAGES_PATH = os.path.join('images', 'categories')

def saving_the_category_icon(instance, filename: str) -> str:
    """
    Сохранение иконки категории товаров
    """

    if instance.parent:  # Сохранение изображения для дочерней категории товара
        return os.path.join(IMAGES_PATH, 'icons', f'{instance.parent.slug}', f'{instance.slug}', f'{filename}')

    return os.path.join(IMAGES_PATH, 'icons', f'{instance.slug}', f'{filename}')


def saving_the_category_image(instance, filename: str) -> str:
    """
    Сохранение изображения категории товаров
    """
    return os.path.join(IMAGES_PATH, 'images', f'{instance.slug}', f'{filename}')
