import re

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from loguru import logger
from datetime import time

from src.bot.filters import WhiteListFilter

from src.utils import JsonReader, Config
from src.lang import STRINGS

lang = "ru"

data_path = "data/data.json"
config_path = "data/config.json"

link_pattern = r"[\"\']*https://t\.me/[+a-zA-Z0-9]*[\"\']*|[\"\']*t\.me/[@+a-zA-Z0-9]*[\"\']*"


class AddState(StatesGroup):
    waiting_post = State()
    waiting_chat = State()


def to_int(_time: str) -> int | None:
    try:
        return int(_time)
    except ValueError:
        return None


def to_list(_time: str, separator: str) -> list[str] | None:
    try:
        times = _time.split(separator)
        for item in times:
            time.fromisoformat(item)
    except ValueError:
        return None


def validate_time(_time: str) -> int | list | None:
    time_int = to_int(_time)
    if time_int is not None:
        return time_int

    time_list = to_list(_time, ",")
    if time_list is not None:
        return time_list

    return None


router = Router()
router.message.filter(WhiteListFilter())


@router.message(AddState.waiting_post)
async def waiting_post(message: Message, state: FSMContext, bot: Bot):
    posts: list[dict] = JsonReader.read(data_path, False)

    if message.photo:
        await bot.download(message.photo[-1], destination=f"data/images/{message.photo[-1].file_id}.jpg")
        posts.append({"message": message.caption, "file": f"data/images/{message.photo[-1].file_id}.jpg"})
    else:
        posts.append({"message": message.text, "file": None})

    JsonReader.write(posts, data_path, True, ("src.bot.routes.add", "waiting_post"))

    await message.answer(STRINGS[lang]["posts_number"].format(number=len(posts)))
    await state.clear()


@router.message(AddState.waiting_chat)
async def waiting_chat(message: Message, state: FSMContext):
    chats = Config(**JsonReader.read(config_path, False)).chats

    if re.search(link_pattern, message.text) is None:
        await message.answer(STRINGS[lang]["bad_link"])
        logger.warning(STRINGS["debug"]["bad_link"].format(username=message.from_user.username))
        return None

    link = re.search(link_pattern, message.text).group()
    _time = validate_time(message.text.replace(link, "").replace(":", "", 1).replace(" ", ""))

    if _time is None:
        await message.answer(STRINGS[lang]["bad_time"])
        logger.warning(STRINGS["debug"]["bad_time"].format(username=message.from_user.username))
        return None

    chats[link.replace('"', "").replace("'", "")] = _time

    config = JsonReader.read(config_path, False)
    config["chats"] = chats

    JsonReader.write(config, config_path, True, ("src.bot.routes.add", "waiting_chat"))

    await message.answer(STRINGS[lang]["posts_number"].format(number=len(chats)))
    await state.clear()


@router.message(Command("add", "добавить"))
async def add(message: Message, command: CommandObject, state: FSMContext):
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

    async def add_post():
        await message.answer(STRINGS[lang]["add_post"])
        await state.set_state(AddState.waiting_post)

    async def add_chat():
        await message.answer(STRINGS[lang]["add_chat"])
        await state.set_state(AddState.waiting_chat)

    argument = command.args

    actions = {
        "post": add_post,
        "chat": add_chat,
        "пост": add_post,
        "чат": add_chat
    }

    await actions[argument]()
