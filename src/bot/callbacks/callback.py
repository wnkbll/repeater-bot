from aiogram.filters.callback_data import CallbackData


class Callback(CallbackData, prefix="callback"):
    action: str
    index: int | str
