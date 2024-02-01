from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery

from src.bot.routes import posts, chats, sleep
from src.bot.callbacks import Callback
from src.bot.keyboards import StartKeyboard
from src.bot.filters import WhiteListFilter

from src.utils import Globals

config_path = Globals.config_path

router = Router()
router.include_routers(posts.router, chats.router, sleep.router)
router.message.filter(WhiteListFilter())


# TODO Добавить строки локализации

@router.callback_query(Callback.filter((F.subject == "start") & (F.action == "back")))
async def on_back_callback(query: CallbackQuery):
    keyboard = StartKeyboard().builder
    await query.message.edit_text("Что хотите поменять?", reply_markup=keyboard.as_markup())


@router.message(Command("start"))
async def start(message: Message):
    keyboard = StartKeyboard().builder
    await message.answer("Что хотите поменять?", reply_markup=keyboard.as_markup())
