from aiogram.types import InlineKeyboardButton

from src.bot.keyboards import Keyboard
from src.bot.callbacks import PostsCallback

from src.lang import STRINGS

lang = "ru"


class PostsKeyboard(Keyboard):
    def __init__(self, amount_of_buttons: int, action: str):
        super().__init__(amount_of_buttons, action)

        self.add_buttons()
        self.adjust_buttons()

    def add_buttons(self):
        for index in range(self.amount_of_buttons):
            button = InlineKeyboardButton(text=f"{index + 1}", callback_data=PostsCallback(action=self.action, index=index).pack())
            self.builder.add(button)

        all_button = InlineKeyboardButton(text=STRINGS[lang]["all"], callback_data=PostsCallback(action=self.action, index=self.amount_of_buttons + 1).pack())
        self.builder.add(all_button)

    def get_row_size(self) -> int:
        if self.amount_of_buttons <= 5:
            return self.amount_of_buttons
        elif self.amount_of_buttons % 2 == 0:
            return int(self.amount_of_buttons / 2)
        else:
            return int(self.amount_of_buttons / 2) + 1

    def adjust_buttons(self) -> None:
        row_size = self.get_row_size()

        if row_size < 10:
            self.builder.adjust(row_size, repeat=True)
        else:
            self.builder.adjust(9, repeat=True)
