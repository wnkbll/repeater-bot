from aiogram.filters.callback_data import CallbackData


class ChatsCallback(CallbackData, prefix="chats"):
    action: str
    chat: str
