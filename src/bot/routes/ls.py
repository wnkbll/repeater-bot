from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message, FSInputFile

from loguru import logger

from src.bot.callbacks import PostsCallback
from src.bot.filters import WhiteListFilter
from src.bot.keyboards import PostsKeyboard
from src.utils import Config, JsonReader
from src.lang import STRINGS

lang = "ru"

config_path = "data/config.json"
data_path = "data/data.json"

router = Router()
router.message.filter(WhiteListFilter())


@router.callback_query(PostsCallback.filter(F.action == "ls"))
async def ls_callback(query: CallbackQuery, callback_data: PostsCallback):
    posts: list[dict] = JsonReader.read(data_path, False)
    index = callback_data.index

    if index != "all":
        if posts[index]["file"]:
            image = FSInputFile(posts[index]["file"])
            await query.message.answer_photo(image, caption=posts[index]["message"])
            await query.message.delete()

            return

        await query.message.answer(posts[index]["message"])
        await query.message.delete()

        return

    for post in posts:
        if post["file"]:
            image = FSInputFile(post["file"])
            await query.message.answer_photo(image, caption=post["message"])
        else:
            await query.message.answer(post["message"])

    await query.message.delete()


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
        posts: list[dict] = JsonReader.read(data_path, False)
        posts_length = len(posts)

        if posts_length <= 0:
            await message.answer(STRINGS[lang]["empty_list"])
            return

        if posts_length == 1:
            if posts[0]["file"]:
                image = FSInputFile(posts[0]["file"])
                await message.answer_photo(image, caption=posts[0]["message"])

                return

            await message.answer(posts[0]["message"])
            return

        builder = PostsKeyboard(posts_length, "ls").builder

        await message.answer(STRINGS[lang]["choose_post"], reply_markup=builder.as_markup())

    async def list_chats():
        chats = Config(**JsonReader.read(config_path, False)).chats
        if len(chats) < 1:
            await message.answer(STRINGS[lang]["empty_chats"], parse_mode="Markdown")
            return None

        answer = ""
        for index, item in enumerate(chats.items()):
            answer += f"{index + 1}) {item[0]}: {item[1]}\n"

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
