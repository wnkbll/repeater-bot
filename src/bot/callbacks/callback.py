from aiogram.filters.callback_data import CallbackData


class Callback(CallbackData, prefix="callback"):
    subject: str
    action: str
    index: int | str
