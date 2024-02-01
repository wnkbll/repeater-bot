from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Sized

from src.bot.callbacks import Callback


class StartKeyboard:
    def __init__(self):
        self.builder = InlineKeyboardBuilder()

        # TODO Добавить строки локализации
        posts_button = InlineKeyboardButton(text="Список постов", callback_data=Callback(subject="start", action="posts", index=0).pack())
        chats_button = InlineKeyboardButton(text="Список чатов", callback_data=Callback(subject="start", action="chats", index=1).pack())
        sleep_button = InlineKeyboardButton(text="Время сна", callback_data=Callback(subject="start", action="sleep", index=2).pack())

        buttons = [posts_button, chats_button, sleep_button]

        for button in buttons:
            self.builder.add(button)

        self.builder.adjust(3, repeat=True)


class PostsKeyboard:
    def __init__(self):
        self.builder = InlineKeyboardBuilder()

        # TODO Добавить строки локализации
        add_button = InlineKeyboardButton(text="Добавить пост", callback_data=Callback(subject="posts", action="add", index=0).pack())
        edit_button = InlineKeyboardButton(text="Изменить пост", callback_data=Callback(subject="posts", action="edit", index=1).pack())
        delete_button = InlineKeyboardButton(text="Удалить пост", callback_data=Callback(subject="posts", action="delete", index=2).pack())
        list_button = InlineKeyboardButton(text="Список постов", callback_data=Callback(subject="posts", action="list", index=3).pack())
        back_button = InlineKeyboardButton(text="<< Назад", callback_data=Callback(subject="start", action="back", index=4).pack())

        buttons = [add_button, edit_button, delete_button, list_button, back_button]

        for button in buttons:
            self.builder.add(button)

        self.builder.adjust(2, repeat=True)


class ChatsKeyboard:
    def __init__(self):
        self.builder = InlineKeyboardBuilder()

        # TODO Добавить строки локализации
        add_button = InlineKeyboardButton(text="Добавить чат", callback_data=Callback(subject="chats", action="add", index=0).pack())
        edit_button = InlineKeyboardButton(text="Изменить чат", callback_data=Callback(subject="chats", action="edit", index=1).pack())
        delete_button = InlineKeyboardButton(text="Удалить чат", callback_data=Callback(subject="chats", action="delete", index=2).pack())
        list_button = InlineKeyboardButton(text="Список чатов", callback_data=Callback(subject="chats", action="list", index=3).pack())
        back_button = InlineKeyboardButton(text="<< Назад", callback_data=Callback(subject="start", action="back", index=4).pack())

        buttons = [add_button, edit_button, delete_button, list_button, back_button]

        for button in buttons:
            self.builder.add(button)

        self.builder.adjust(2, repeat=True)


class SleepKeyboard:
    def __init__(self):
        self.builder = InlineKeyboardBuilder()
        edit_button = InlineKeyboardButton(text="Изменить время", callback_data=Callback(subject="sleep", action="edit", index=0).pack())
        list_button = InlineKeyboardButton(text="Посмотреть время", callback_data=Callback(subject="sleep", action="list", index=1).pack())
        back_button = InlineKeyboardButton(text="<< Назад", callback_data=Callback(subject="start", action="back", index=2).pack())

        buttons = [edit_button, list_button, back_button]

        for button in buttons:
            self.builder.add(button)

        self.builder.adjust(2, repeat=True)


class BackKeyboard:
    def __init__(self, subject: str):
        self.builder = InlineKeyboardBuilder()

        # TODO Добавить строки локализации
        back_button = InlineKeyboardButton(text="<< Назад", callback_data=Callback(subject=subject, action="back", index=0).pack())

        self.builder.add(back_button)
        self.builder.adjust(1, repeat=True)


class SleepEditKeyboard:
    def __init__(self):
        self.builder = InlineKeyboardBuilder()

        # TODO Добавить строки локализации
        start_button = InlineKeyboardButton(text="Начало сна", callback_data=Callback(subject="sleep", action="start", index=0).pack())
        stop_button = InlineKeyboardButton(text="Окончание сна", callback_data=Callback(subject="sleep", action="stop", index=1).pack())
        back_button = InlineKeyboardButton(text="<< Назад", callback_data=Callback(subject="sleep", action="back", index=2).pack())

        buttons = [start_button, stop_button, back_button]

        for button in buttons:
            self.builder.add(button)

        self.builder.adjust(2, repeat=True)


class NumbersKeyboard:
    def __init__(self, subject: str, action: str, collection: Sized, is_all_button: bool = False):
        self.builder = InlineKeyboardBuilder()

        # TODO Добавить строки локализации

        chats_length = len(collection)

        for index in range(chats_length):
            button = InlineKeyboardButton(text=f"{index + 1}", callback_data=Callback(subject=subject, action=action, index=index).pack())
            self.builder.add(button)

        if is_all_button:
            all_button = InlineKeyboardButton(text="Все", callback_data=Callback(subject=subject, action=action, index="all").pack())
            self.builder.add(all_button)

        back_button = InlineKeyboardButton(text="<< Назад", callback_data=Callback(subject=action, action="back", index=chats_length + 1).pack())
        self.builder.add(back_button)

        if chats_length <= 8:
            row_size = chats_length
        elif chats_length % 2 == 0:
            row_size = int(chats_length / 2)
        else:
            row_size = int(chats_length / 2) + 1

        self.builder.adjust(row_size if row_size < 9 else 8, 1, 1, repeat=True)
