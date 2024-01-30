from aiogram.types import InlineKeyboardButton

from src.bot.keyboards import Keyboard
from src.bot.callbacks import HelpCallback


class HelpKeyboard(Keyboard):
    def __init__(self):
        super().__init__(4, "help")

        self.add_buttons()
        self.adjust_buttons()

    def add_buttons(self):
        add_button = InlineKeyboardButton(text="add", callback_data=HelpCallback(action=self.action, index="all").pack())
        ls_button = InlineKeyboardButton(text="ls", callback_data=HelpCallback(action=self.action, index="ls").pack())
        edit_button = InlineKeyboardButton(text="edit", callback_data=HelpCallback(action=self.action, index="edit").pack())
        remove_button = InlineKeyboardButton(text="remove", callback_data=HelpCallback(action=self.action, index="remove").pack())

        button = [add_button, ls_button, edit_button, remove_button]

        self.builder.add(button)

    def adjust_buttons(self):
        self.builder.adjust(self.amount_of_buttons, repeat=True)
