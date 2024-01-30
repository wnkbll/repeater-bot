from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

from loguru import logger

from src.bot.callbacks import HelpCallback
from src.bot.keyboards import HelpKeyboard
from src.bot.filters import WhiteListFilter
from src.utils import Globals
from src.lang import STRINGS

lang = Globals.lang

router = Router()
router.message.filter(WhiteListFilter())


@router.callback_query(HelpCallback.filter(F.action == "help"))
async def _help_callback(query: CallbackQuery, callback_data: HelpCallback):
    pass


@router.message(Command("help", "помощь"))
async def _help(message: Message, command: CommandObject):
    if command.args is not None:
        await message.answer(STRINGS[lang]["unexpected_args"])
        logger.warning(STRINGS["debug"]["unexpected_args"].format(username=message.from_user.username))
        return None

    builder = HelpKeyboard().builder
    await message.answer("Выберите команду", reply_markup=builder.as_markup())
