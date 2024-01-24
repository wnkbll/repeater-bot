from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from loguru import logger

from src.bot.filters import WhiteListFilter
from src.utils import Config, JsonReader
from src.lang import STRINGS

lang = "ru"

config_path = "data/config.json"
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

    if command.args not in arguments:
        await message.answer(STRINGS[lang]["unexpected_args"])
        logger.warning(STRINGS["debug"]["unexpected_args"].format(username=message.from_user.username))
        return None

    async def list_posts():
        pass

    async def list_chats():
        chats = Config(**JsonReader.read(config_path, False)).chats
        if len(chats) < 1:
            await message.answer("Нет чатов", parse_mode="Markdown")  # TODO Нужна новая строка
            return None

        answer = ""
        for item in chats.items():
            answer += f"{item[0]}: {item[1]}\n"

        await message.answer(f"```\n{answer}```", parse_mode="Markdown")

    async def list_sleep():
        sleep = Config(**JsonReader.read(config_path, False)).sleep

        answer = ""
        for item in sleep.items():
            answer += f"{item[0]}: {item[1]}\n"

        await message.answer(f"```\n{answer}```", parse_mode="Markdown")

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
