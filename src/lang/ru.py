BOT: dict[str, str] = {
    "start": "Проверка пройдена.",
    "posts_number": "Текущее количество постов: {number}.",
    "add_post": "Отправьте новый пост.",
    "empty_list": "Список постов пустой.",
    "choose_post": "Выберите пост",
    "all": "Все",
    "post_edited": "Пост №{number} обновлён.",
    "send_edited": "Отправьте обновлённый пост.",
    "no_permissions": "У вас недостаточно прав.",
    "add_chat": "Отправьте новый чат.",
    "unexpected_args": "Вы ввели неправильные аргументы.",
    "bad_link": "Ссылка не обнаружена.",
    "bad_time": "Время не обнаружено."
}

CLIENT: dict[str, str] = {
    "post_sent": "Сообщение в канал {title} отправлено."
}


def register(strings: dict) -> dict[str, dict[str, str]]:
    lang = "ru"
    strings[lang] = {}

    for item in BOT.items():
        strings[lang][item[0]] = item[1]

    for item in CLIENT.items():
        strings[lang][item[0]] = item[1]

    return strings
