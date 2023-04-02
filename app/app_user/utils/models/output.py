def output_name(profile) -> str:
    """ Вывод имени пользователя """

    if profile.full_name:
        return f'{profile.full_name}'

    elif profile.user.first_name:
        return f'{profile.user.first_name} {profile.user.last_name}'

    else:
        return f'{profile.user.username}'
