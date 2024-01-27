from aiogram.filters.callback_data import CallbackData


class SleepCallback(CallbackData, prefix="sleep"):
    action: str
    index: str
