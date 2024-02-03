import re

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from loguru import logger

from src.bot.callbacks import Callback
from src.bot.keyboards import ChatsKeyboard, BackKeyboard, NumbersKeyboard
from src.bot.filters import WhiteListFilter

from src.utils import Config, JsonReader, Dictionaries, TimeValidator, Globals

config_path = Globals.config_path

router = Router()
router.message.filter(WhiteListFilter())


class ChatsState(StatesGroup):
    waiting_add = State()
    waiting_edit = State()


# TODO Добавить строки локализации

@router.message(ChatsState.waiting_add)
async def on_waiting_add_chat(message: Message, state: FSMContext):
    link_pattern = Globals.link_pattern

    if re.search(link_pattern, message.text) is None:
        await message.answer("Ссылка не найдена")
        logger.warning(f"Неверная ссылка от {message.from_user.username}")
        return None

    link = re.search(link_pattern, message.text).group()
    time = TimeValidator(message.text.replace(link, "").replace(":", "", 1).replace(" ", "")).validate_time()

    if time is None:
        await message.answer("Неверное время")
        logger.warning(f"Неверное время от {message.from_user.username}")
        return None

    config = Config(**JsonReader.read(config_path, False))
    config.chats[link.replace('"', "").replace("'", "")] = time

    JsonReader.write(config.model_dump(), config_path, False)

    keyboard = BackKeyboard("chats").builder

    chats_list = ""
    for index, item in enumerate(config.chats.items()):
        chats_list += f"{index + 1}) {item[0]}: {item[1]}\n"

    await message.answer(f"Текущий список чатов:\n```Chats\n{chats_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")
    await state.clear()


@router.callback_query(Callback.filter((F.subject == "chats") & (F.action == "add")))
async def on_chat_add_callback(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Добавьте новый чат в формате {ссылка}: {время}.\nВремя должно быть числом или последовательностью в формате {HH:mm, HH:mm}")
    await state.set_state(ChatsState.waiting_add)


@router.message(ChatsState.waiting_edit)
async def on_waiting_edit_chat(message: Message, state: FSMContext):
    time = TimeValidator(message.text.replace(" ", "")).validate_time()

    if time is None:
        await message.answer("Неверное время")
        logger.warning(f"Неверное время от {message.from_user.username}")
        return None

    user_data = await state.get_data()

    config = Config(**JsonReader.read(config_path, False))
    chat_link = Dictionaries.get_key(config.chats, user_data["index"])

    config.chats[chat_link] = time

    JsonReader.write(config.model_dump(), config_path, False)

    keyboard = BackKeyboard("chats").builder

    chats_list = ""
    for index, item in enumerate(config.chats.items()):
        chats_list += f"{index + 1}) {item[0]}: {item[1]}\n"

    await message.answer(f"Текущий список чатов:\n```Chats\n{chats_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")
    await state.clear()


@router.callback_query(Callback.filter((F.subject == "edit") & (F.action == "chats")))
async def on_chat_edit_number_callback(query: CallbackQuery, callback_data: Callback, state: FSMContext):
    await query.message.edit_text("Введите новое время для этого чата.\nВремя должно быть числом или последовательностью в формате {HH:mm, HH:mm}")
    await state.update_data(index=callback_data.index)
    await state.set_state(ChatsState.waiting_edit)


@router.callback_query(Callback.filter((F.subject == "chats") & (F.action == "edit")))
async def on_chat_edit_callback(query: CallbackQuery):
    config = Config(**JsonReader.read(config_path, False))

    keyboard = NumbersKeyboard("edit", "chats", config.chats).builder

    chats_list = ""
    for index, item in enumerate(config.chats.items()):
        chats_list += f"{index + 1}) {item[0]}: {item[1]}\n"

    await query.message.edit_text(f"Выберите чат, который вы хотите изменить: \n```Chats\n{chats_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "delete") & (F.action == "chats")))
async def on_chat_delete_number_callback(query: CallbackQuery, callback_data: Callback):
    config = Config(**JsonReader.read(config_path, False))
    chat_link = Dictionaries.get_key(config.chats, callback_data.index)
    config.chats.pop(chat_link)
    JsonReader.write(config.model_dump(), config_path, False)

    keyboard = BackKeyboard("chats").builder

    chats_list = ""
    for index, item in enumerate(config.chats.items()):
        chats_list += f"{index + 1}) {item[0]}: {item[1]}\n"

    await query.message.edit_text(f"Текущий список чатов:\n```Chats\n{chats_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "chats") & (F.action == "delete")))
async def on_chat_delete_callback(query: CallbackQuery):
    config = Config(**JsonReader.read(config_path, False))

    keyboard = NumbersKeyboard("delete", "chats", config.chats).builder

    chats_list = ""
    for index, item in enumerate(config.chats.items()):
        chats_list += f"{index + 1}) {item[0]}: {item[1]}\n"

    await query.message.edit_text(f"Выберите чат, который вы хотите изменить: \n```Chats\n{chats_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "chats") & (F.action == "list")))
async def on_chat_list_callback(query: CallbackQuery):
    keyboard = BackKeyboard("chats").builder

    chats = Config(**JsonReader.read(config_path, False)).chats
    if len(chats) < 1:
        await query.message.edit_text("Список чатов пустой.", reply_markup=keyboard.as_markup())
        return None

    chats_list = ""
    for index, item in enumerate(chats.items()):
        chats_list += f"{index + 1}) {item[0]}: {item[1]}\n"

    await query.message.edit_text(f"```Chats\n{chats_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "chats") & (F.action == "back")))
async def on_chats_back_callback(query: CallbackQuery):
    keyboard = ChatsKeyboard().builder
    await query.message.edit_text("Что хотите сделать с чатами?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "start") & (F.action == "chats")))
async def on_chats_callback(query: CallbackQuery):
    keyboard = ChatsKeyboard().builder
    await query.message.edit_text("Что хотите сделать с чатами?", reply_markup=keyboard.as_markup())
