from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.filters import WhiteListFilter
from src.lang import STRINGS

lang = "ru"

router = Router()
router.message.filter(WhiteListFilter())


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(STRINGS[lang]["start"])
