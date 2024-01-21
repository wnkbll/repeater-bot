from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from loguru import logger

from src.bot.filters import WhiteListFilter
from src.lang import STRINGS

lang = "ru"

data_path = "data/data.json"

router = Router()
router.message.filter(WhiteListFilter())


@router.message(Command("ls", "list", "список"))
async def ls(message: Message, command: CommandObject):
    arguments = [
        "posts",
        "chats",
        "sleep",
        "постов",
        "чатов",
        "сна"
    ]

    if command.args not in arguments or len(command.args.split()) > 1:
        await message.answer(STRINGS[lang]["unexpected_args"])
        logger.warning(STRINGS["debug"]["unexpected_args"].format(username=message.from_user.username))
        return None

    async def list_posts():
        pass

    async def list_chats():
        pass

    async def list_sleep():
        pass

    argument = command.args

    actions = {
        "posts": list_posts,
        "chats": list_chats,
        "sleep": list_sleep,
        "постов": list_posts,
        "чатов": list_chats,
        "сна": list_sleep
    }

    await actions[argument]()
