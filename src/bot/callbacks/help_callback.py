from aiogram.filters.callback_data import CallbackData


class HelpCallback(CallbackData, prefix="help_command"):
    action: str
    index: str
