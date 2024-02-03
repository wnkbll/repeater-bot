BOT: dict[str, str] = {
    "on_start_command": "Что хотите поменять?",

    "on_posts_command": "Что хотите сделать с постами?",
    "on_posts_edit_callback": "Выберите пост, который хотите изменить.",
    "on_posts_edit_waiting": "Отправьте изменённый пост.\nМожно приложить не больше одного изображения.",
    "on_posts_list_callback": "Выберите пост, который хотите посмотреть.",
    "on_posts_delete_callback": "Выберите пост, который хотите удалить.",
    "current_posts_number": "Текущее количество постов",

    "on_chats_command": "Что хотите сделать с чатами?",
    "on_chats_add_callback": "Добавьте новый чат в формате {ссылка}: {время}.\nВремя должно быть числом или последовательностью в формате {HH:mm, HH:mm}",
    "on_chats_edit_callback": "Выберите чат, который вы хотите изменить",
    "on_chats_edit_waiting": "Введите новое время для этого чата.\nВремя должно быть числом или последовательностью в формате {HH:mm, HH:mm}",
    "on_chats_delete_callback": "Выберите чат, который вы хотите удалить",
    "current_chats": "Текущий список чатов",

    "on_sleep_command": "Что хотите сделать со временем сна?",
    "on_sleep_edit_start": "Отправьте новое время начала сна в формате HH:mm. Например, 22:15.",
    "on_sleep_edit_stop": "Отправьте новое время окончания сна в формате HH:mm. Например, 22:15.",
    "current_sleep_time": "Текущее время сна",

    "on_emtpy_posts_list": "Список постов пустой.",
    "on_empty_chats_list": "Список чатов пустой.",

    "on_bad_time": "Вы ввели неправильное время",
    "on_bad_link": "Вы ввели неправильную ссылку",
}

BUTTONS: dict[str, str] = {
    "start_posts_button": "Список постов",
    "start_chats_button": "Список чатов",
    "start_sleep_button": "Время сна",

    "add_posts_button": "Добавить пост",
    "edit_posts_button": "Изменить пост",
    "delete_posts_button": "Удалить пост",
    "list_posts_button": "Список постов",

    "add_chats_button": "Добавить чат",
    "edit_chats_button": "Изменить чат",
    "delete_chats_button": "Удалить чат",
    "list_chats_button": "Список чатов",

    "edit_sleep_button": "Изменить время",
    "list_sleep_button": "Посмотреть время",

    "edit_start_sleep_button": "Начало сна",
    "edit_end_sleep_button": "Окончание сна",

    "all_button": "Все",
    "back_button": "<< Назад",
}

CLIENT: dict[str, str] = {
    "post_sent": "Сообщение в канал {title} отправлено.",
}


def register(strings: dict) -> dict[str, dict[str, str]]:
    lang = "ru"
    strings[lang] = {}

    for item in BOT.items():
        strings[lang][item[0]] = item[1]

    for item in BUTTONS.items():
        strings[lang][item[0]] = item[1]

    for item in CLIENT.items():
        strings[lang][item[0]] = item[1]

    return strings
