import os.path


IMAGES_PATH = os.path.join("images", "profiles")


def save_avatar(instance, filename: str) -> str:
    """
    Функция для сохранения аватара пользователя

    @param instance: объект профайла
    @param filename: название файла
    @return: path
    """
    return os.path.join(
        IMAGES_PATH, f"{instance.user.username}", "avatar", f"{filename}"
    )
