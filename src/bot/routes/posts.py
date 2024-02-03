import os

from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.bot.callbacks import Callback
from src.bot.keyboards import PostsKeyboard, NumbersKeyboard, BackKeyboard
from src.bot.filters import WhiteListFilter

from src.utils import JsonReader, Globals

config_path = Globals.config_path
data_path = Globals.data_path

router = Router()
router.message.filter(WhiteListFilter())


class PostState(StatesGroup):
    waiting_add = State()
    waiting_edit = State()


# TODO Добавить строки локализации

@router.message(PostState.waiting_add)
async def on_waiting_add_post(message: Message, state: FSMContext, bot: Bot):
    posts: list[dict] = JsonReader.read(data_path, False)

    if message.photo:
        await bot.download(message.photo[-1], destination=f"data/images/{message.photo[-1].file_id}.jpg")
        posts.append({"message": message.caption, "file": f"data/images/{message.photo[-1].file_id}.jpg"})
    else:
        posts.append({"message": message.text, "file": None})

    JsonReader.write(posts, data_path, False)
    await state.clear()

    keyboard = PostsKeyboard().builder
    await message.answer(f"Текущее количество постов: {len(posts)}.\n\nЧто хотите сделать с постами?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "posts") & (F.action == "add")))
async def on_posts_add_callback(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Отправьте новый пост.\nМожно приложить не больше одного изображения.")
    await state.set_state(PostState.waiting_add)


@router.message(PostState.waiting_edit)
async def on_waiting_edit_post(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    index = int(user_data["index"])

    posts: list[dict] = JsonReader.read(data_path, False)

    if posts[index]["file"]:
        os.remove(posts[index]["file"])

    if message.photo:
        await bot.download(message.photo[-1], destination=f"data/images/{message.photo[-1].file_id}.jpg")
        posts[index] = {"message": message.caption, "file": f"data/images/{message.photo[-1].file_id}.jpg"}
    else:
        posts[index] = {"message": message.text, "file": None}

    JsonReader.write(posts, data_path, False)
    await state.clear()

    keyboard = PostsKeyboard().builder
    await message.answer(f"Текущее количество постов: {len(posts)}.\n\nЧто хотите сделать с постами?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "edit") & (F.action == "posts")))
async def on_posts_edit_numbers_callback(query: CallbackQuery, callback_data: Callback, state: FSMContext):
    await query.message.edit_text("Отправьте изменённый пост.\nМожно приложить не больше одного изображения.")
    await state.update_data(index=callback_data.index)
    await state.set_state(PostState.waiting_edit)


@router.callback_query(Callback.filter((F.subject == "posts") & (F.action == "edit")))
async def on_posts_edit_callback(query: CallbackQuery):
    posts: list[dict] = JsonReader.read(data_path, False)

    if len(posts) == 0:
        keyboard = BackKeyboard("posts").builder
        await query.message.edit_text("Список постов пустой", reply_markup=keyboard.as_markup())
        return None

    keyboard = NumbersKeyboard("edit", "posts", posts).builder
    await query.message.edit_text("Выберите пост, который хотите изменить.", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "delete") & (F.action == "posts")))
async def on_posts_delete_numbers_callback(query: CallbackQuery, callback_data: Callback):
    keyboard = PostsKeyboard().builder

    posts: list[dict] = JsonReader.read(data_path, False)
    index = callback_data.index

    if index != "all":
        _index = int(index)
        if posts[_index]["file"]:
            os.remove(posts[_index]["file"])
        posts.pop(_index)
        JsonReader.write(posts, data_path, False)
        await query.message.edit_text(f"Текущее количество постов: {len(posts)}.\n\nЧто хотите сделать с постами?", reply_markup=keyboard.as_markup())
        return None

    for post in posts:
        if post["file"]:
            os.remove(post["file"])

    JsonReader.write([], data_path, False)
    await query.message.edit_text("Текущее количество постов: 0.\n\nЧто хотите сделать с постами?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "posts") & (F.action == "delete")))
async def on_posts_delete_callback(query: CallbackQuery):
    posts: list[dict] = JsonReader.read(data_path, False)

    if len(posts) == 0:
        keyboard = BackKeyboard("posts").builder
        await query.message.edit_text("Список постов пустой", reply_markup=keyboard.as_markup())
        return None

    keyboard = NumbersKeyboard("delete", "posts", posts, is_all_button=True).builder
    await query.message.edit_text("Выберите пост, который хотите удалить.", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "list") & (F.action == "posts")))
async def on_posts_list_numbers_callback(query: CallbackQuery, callback_data: Callback):
    keyboard = PostsKeyboard().builder

    posts: list[dict] = JsonReader.read(data_path, False)
    index = callback_data.index

    if index != "all":
        _index = int(index)
        if posts[_index]["file"]:
            image = FSInputFile(posts[_index]["file"])
            await query.message.answer_photo(image, caption=posts[_index]["message"])
            await query.message.delete()

            return None

        await query.message.answer(posts[_index]["message"])

        await query.message.delete()
        await query.message.answer("Что хотите сделать с постами?", reply_markup=keyboard.as_markup())

        return None

    for post in posts:
        if post["file"]:
            image = FSInputFile(post["file"])
            await query.message.answer_photo(image, caption=post["message"])
        else:
            await query.message.answer(post["message"])

    await query.message.delete()
    await query.message.answer("Что хотите сделать с постами?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "posts") & (F.action == "list")))
async def on_posts_list_callback(query: CallbackQuery):
    posts: list[dict] = JsonReader.read(data_path, False)
    if len(posts) == 0:
        keyboard = BackKeyboard("posts").builder
        await query.message.edit_text("Список постов пустой", reply_markup=keyboard.as_markup())
        return None

    keyboard = NumbersKeyboard("list", "posts", posts, is_all_button=True).builder
    await query.message.edit_text("Выберите пост, который хотите удалить.", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "posts") & (F.action == "back")))
async def on_posts_back_callback(query: CallbackQuery):
    keyboard = PostsKeyboard().builder
    await query.message.edit_text("Что хотите сделать с постами?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "start") & (F.action == "posts")))
async def on_posts_callback(query: CallbackQuery):
    keyboard = PostsKeyboard().builder
    await query.message.edit_text("Что хотите сделать с постами?", reply_markup=keyboard.as_markup())
