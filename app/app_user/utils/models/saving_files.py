import os.path


IMAGES_PATH = os.path.join('images', 'profiles')

def save_avatar(instance, filename: str) -> str:
    """ Сохранение аватара пользователя """

    return os.path.join(IMAGES_PATH, f'{instance.user.username}', 'avatar', f'{filename}')
