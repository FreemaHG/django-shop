import os.path


CATEGORIES_PATH = os.path.join('images', 'categories')
PRODUCTS_PATH = os.path.join('images', 'products')

def saving_the_category_icon(instance, filename: str) -> str:
    """
    Сохранение иконки категории товаров
    """

    if instance.parent:  # Сохранение изображения для дочерней категории товара
        return os.path.join(CATEGORIES_PATH, 'icons', f'{instance.parent.slug}', f'{instance.slug}', f'{filename}')

    return os.path.join(CATEGORIES_PATH, 'icons', f'{instance.slug}', f'{filename}')


def saving_the_category_image(instance, filename: str) -> str:
    """
    Сохранение изображения категории товаров
    """
    return os.path.join(CATEGORIES_PATH, 'images', f'{instance.slug}', f'{filename}')


def saving_images_for_product(instance, filename: str) -> str:
    """
    Сохранение изображения товара
    """
    # TODO проверить корректность работы instance.product.id!!!
    return os.path.join(PRODUCTS_PATH, f'{instance.product.id}', f'{filename}')
