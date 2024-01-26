from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from loguru import logger

from src.bot.filters import WhiteListFilter
from src.lang import STRINGS

lang = "ru"

config_path = "data/config.json"
data_path = "data/data.json"

router = Router()
router.message.filter(WhiteListFilter())


@router.message(Command("edit", "изменить", "редактировать"))
async def edit(message: Message, command: CommandObject):
    arguments = [
        "posts",
        "chats",
        "sleep",
        "посты",
        "чаты",
        "сон"
    ]

    if command.args not in arguments:
        await message.answer(STRINGS[lang]["unexpected_args"])
        logger.warning(STRINGS["debug"]["unexpected_args"].format(username=message.from_user.username))
        return None

    async def edit_posts():
        pass

    async def edit_chats():
        pass

    async def edit_sleep():
        pass

    argument = command.args

    actions = {
        "posts": edit_posts,
        "chats": edit_chats,
        "sleep": edit_sleep,
        "посты": edit_posts,
        "чаты": edit_chats,
        "сон": edit_sleep
    }

    await actions[argument]()
