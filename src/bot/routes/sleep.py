from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from loguru import logger

from src.bot.callbacks import Callback
from src.bot.keyboards import SleepKeyboard, BackKeyboard, SleepEditKeyboard
from src.bot.filters import WhiteListFilter

from src.utils import Config, JsonReader, TimeValidator, Globals

config_path = Globals.config_path

router = Router()
router.message.filter(WhiteListFilter())


class SleepState(StatesGroup):
    waiting_sleep = State()


# TODO Добавить строки локализации

@router.message(SleepState.waiting_sleep)
async def on_waiting_sleep(message: Message, state: FSMContext):
    user_data = await state.get_data()
    config = Config(**JsonReader.read(config_path, False))
    time = TimeValidator(message.text).to_string()

    if time is None:
        await message.answer("Вы ввели неправильное время")
        logger.warning(f"Неправильное время от {message.from_user.username}")
        return None

    config.sleep[user_data["action"]] = time
    JsonReader.write(config.model_dump(), config_path, False)

    keyboard = BackKeyboard("sleep").builder

    sleep_list = ""
    for item in config.sleep.items():
        sleep_list += f"{item[0]}: {item[1]}\n"

    await message.answer(f"Текущее время сна:\n```Sleep\n{sleep_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "sleep") & (F.action == "start")))
async def on_sleep_start_edit_callback(query: CallbackQuery, callback_data: Callback, state: FSMContext):
    await query.message.edit_text("Отправьте новое время начала сна в формате HH:mm. Например, 22:15.")
    await state.update_data(action=callback_data.action)
    await state.set_state(SleepState.waiting_sleep)


@router.callback_query(Callback.filter((F.subject == "sleep") & (F.action == "stop")))
async def on_sleep_stop_edit_callback(query: CallbackQuery, callback_data: Callback, state: FSMContext):
    await query.message.edit_text("Отправьте новое время окончания сна в формате HH:mm. Например, 22:15.")
    await state.update_data(action=callback_data.action)
    await state.set_state(SleepState.waiting_sleep)


@router.callback_query(Callback.filter((F.subject == "sleep") & (F.action == "edit")))
async def on_sleep_edit_callback(query: CallbackQuery):
    keyboard = SleepEditKeyboard().builder

    sleep = Config(**JsonReader.read(config_path, False)).sleep

    sleep_list = ""
    for item in sleep.items():
        sleep_list += f"{item[0]}: {item[1]}\n"

    await query.message.edit_text(f"```Sleep\n{sleep_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "sleep") & (F.action == "list")))
async def on_sleep_list_callback(query: CallbackQuery):
    keyboard = BackKeyboard("sleep").builder

    sleep = Config(**JsonReader.read(config_path, False)).sleep

    sleep_list = ""
    for item in sleep.items():
        sleep_list += f"{item[0]}: {item[1]}\n"

    await query.message.edit_text(f"```Sleep\n{sleep_list}```", reply_markup=keyboard.as_markup(), parse_mode="Markdown")


@router.callback_query(Callback.filter((F.subject == "sleep") & (F.action == "back")))
async def on_sleep_back_callback(query: CallbackQuery):
    keyboard = SleepKeyboard().builder
    await query.message.edit_text("Что хотите сделать со временем сна?", reply_markup=keyboard.as_markup())


@router.callback_query(Callback.filter((F.subject == "start") & (F.action == "sleep")))
async def on_sleep_callback(query: CallbackQuery):
    keyboard = SleepKeyboard().builder
    await query.message.edit_text("Что хотите сделать со временем сна?", reply_markup=keyboard.as_markup())
