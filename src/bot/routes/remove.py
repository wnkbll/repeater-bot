import os

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from loguru import logger

from src.bot.callbacks import ChatsCallback, PostsCallback
from src.bot.keyboards import ChatsKeyboard, PostsKeyboard
from src.bot.filters import WhiteListFilter
from src.utils import Config, JsonReader
from src.lang import STRINGS

lang = "ru"

config_path = "data/config.json"
data_path = "data/data.json"

router = Router()
router.message.filter(WhiteListFilter())


@router.message(Command("remove", "delete", "удалить"))
async def remove(message: Message, command: CommandObject):
    arguments = [
        "post",
        "chat",
        "пост",
        "чат"
    ]

    if command.args not in arguments:
        await message.answer(STRINGS[lang]["unexpected_args"])
        logger.warning(STRINGS["debug"]["unexpected_args"].format(username=message.from_user.username))
        return None

    async def remove_post():
        pass

    async def remove_chat():
        pass

    argument = command.args

    actions = {
        "post": remove_post,
        "chat": remove_chat,
        "пост": remove_post,
        "чат": remove_chat
    }

    await actions[argument]()
