from aiogram.filters.callback_data import CallbackData


class PostsCallback(CallbackData, prefix="posts"):
    action: str
    index: int
