from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.bot.filters import WhiteListFilter

from src.utils import JsonReader, Config
from src.lang import STRINGS

lang = "ru"

data_path = "data/data.json"
config_path = "data/config.json"


class AddState(StatesGroup):
    waiting_post = State()
    waiting_chat = State()


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

    splitted_message = message.text.split(":")  # ToDo Добавить валидацию данных

    chats[f"{splitted_message[0]}:{splitted_message[1]}"] = int(splitted_message[2])  # ToDo Добавить поддержку массивов

    config = JsonReader.read(config_path, False)
    config["chats"] = chats

    JsonReader.write(config, config_path, True, ("src.bot.routes.add", "waiting_chat"))

    await message.answer(f"Current number of posts: {len(chats)}.")  # ToDo Нужна новая строка
    await state.clear()


@router.message(Command("add"))
async def add(message: Message, command: CommandObject, state: FSMContext):
    arguments = [
        "post",
        "chat",
        "пост",
        "чат"
    ]

    if command.args not in arguments or len(command.args.split()) > 1:
        await message.answer("Unexpected argument")  # ToDo Нужна новая строка
        return None

    async def add_post():
        await message.answer(STRINGS[lang]["add_post"])
        await state.set_state(AddState.waiting_post)

    async def add_chat():
        await message.answer("Waiting new chat")  # ToDo Нужна новая строка
        await state.set_state(AddState.waiting_chat)

    argument = command.args

    actions = {
        "post": add_post,
        "chat": add_chat,
        "пост": add_post,
        "чат": add_chat
    }

    await actions[argument]()
