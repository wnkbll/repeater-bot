from aiogram.types import InlineKeyboardButton

from src.bot.keyboards import Keyboard
from src.bot.callbacks import SleepCallback


class SleepKeyboard(Keyboard):
    def __init__(self, action: str):
        super().__init__(2, action)

        self.add_buttons()
        self.adjust_buttons()

    def add_buttons(self):
        start_button = InlineKeyboardButton(text="Start", callback_data=SleepCallback(action=self.action, index="start").pack())
        stop_button = InlineKeyboardButton(text="Stop", callback_data=SleepCallback(action=self.action, index="stop").pack())
        self.builder.add(start_button, stop_button)

    def adjust_buttons(self):
        self.builder.adjust(2, repeat=True)
