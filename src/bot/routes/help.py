from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

from src.bot.callbacks import HelpCallback
from src.bot.keyboards import HelpKeyboard
from src.bot.filters import WhiteListFilter
from src.utils import Globals

lang = Globals.lang

router = Router()
router.message.filter(WhiteListFilter())


@router.callback_query(HelpCallback.filter(F.action == "help"))
async def _help_callback(query: CallbackQuery, callback_data: HelpCallback):
    commands = {
        "add": "```add\n/add [arg]. Arg = [post, chat, пост, чат]```",
        "ls": "```ls\n/ls [arg]. Arg = [post, chat, sleep, пост, чат, сон]```",
        "edit": "```edit\n/edit [arg]. Arg = [post, chat, sleep, пост, чат, сон]```",
        "remove": "```remove\n/remove [arg]. Arg = [post, chat, пост, чат]```"
    }

    builder = HelpKeyboard().builder
    await query.message.edit_text(commands[callback_data.index], parse_mode="Markdown", reply_markup=builder.as_markup())


@router.message(Command("help", "помощь"))
async def _help(message: Message):
    builder = HelpKeyboard().builder
    await message.answer("Выберите команду", reply_markup=builder.as_markup())
