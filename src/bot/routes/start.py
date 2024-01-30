from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.filters import WhiteListFilter
from src.utils import Globals
from src.lang import STRINGS

lang = Globals.lang

router = Router()
router.message.filter(WhiteListFilter())


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(STRINGS[lang]["start"])
