import os

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

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


def get_key(dictionary: dict, index: int) -> str:
    for i, key in enumerate(dictionary.keys()):
        if i == index:
            return key


@router.callback_query(PostsCallback.filter(F.action == "remove"))
async def remove_post_callback(query: CallbackQuery, callback_data: PostsCallback):
    posts = JsonReader.read(data_path, False)
    index = callback_data.index

    if index != "all":
        if posts[index]["file"]:
            os.remove(posts[index]["file"])
        posts.pop(index)
        JsonReader.write(posts, data_path, False)
        await query.message.edit_text(STRINGS[lang]["posts_number"].format(number=len(posts)))
        return None

    for post in posts:
        if post["file"]:
            os.remove(post["file"])

    JsonReader.write([], data_path, False)
    await query.message.edit_text(STRINGS[lang]["posts_number"].format(number=0))

    return None


@router.callback_query(ChatsCallback.filter(F.action == "remove"))
async def remove_chat_callback(query: CallbackQuery, callback_data: ChatsCallback):
    chats = Config(**JsonReader.read(config_path, False)).chats
    chat_link = get_key(chats, callback_data.index)
    chats.pop(chat_link)

    config = JsonReader.read(config_path, False)
    config["chats"] = chats

    JsonReader.write(config, config_path, False)

    await query.message.edit_text(STRINGS[lang]["on_chat_remove"].format(link=chat_link), parse_mode="Markdown")


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
        posts = JsonReader.read(data_path, False)

        if len(posts) <= 0:
            await message.answer(STRINGS[lang]["empty_list"])
            return None

        builder = PostsKeyboard(len(posts), "remove").builder
        await message.answer(STRINGS[lang]["choose_post"], reply_markup=builder.as_markup())

    async def remove_chat():
        chats = Config(**JsonReader.read(config_path, False)).chats
        if len(chats) < 1:
            await message.answer(STRINGS[lang]["empty_chats"], parse_mode="Markdown")
            return None

        answer = ""
        for index, item in enumerate(chats.items()):
            answer += f"{index + 1}) {item[0]}: {item[1]}\n"

        builder = ChatsKeyboard(len(chats), "remove", chats).builder
        await message.answer(f"```\n{answer}```", parse_mode="Markdown", reply_markup=builder.as_markup())

    argument = command.args

    actions = {
        "post": remove_post,
        "chat": remove_chat,
        "пост": remove_post,
        "чат": remove_chat
    }

    await actions[argument]()
