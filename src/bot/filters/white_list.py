from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils import Config, JsonReader, Globals

from src.lang import STRINGS

lang = Globals.lang

config_path = Globals.config_path


class WhiteListFilter(BaseFilter):
    def __init__(self):
        self.white_list = Config(**JsonReader.read(config_path, debug=False)).white_list

    async def __call__(self, message: Message) -> bool:
        if message.chat.id in self.white_list or message.from_user.id in self.white_list:
            return True

        await message.answer(STRINGS[lang]["no_permission"])
        return False
