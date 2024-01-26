from aiogram.utils.keyboard import InlineKeyboardBuilder


class Keyboard:
    def __init__(self, amount_of_buttons: int):
        self.builder = InlineKeyboardBuilder()
        self.amount_of_buttons = amount_of_buttons

    def add_buttons(self):
        pass

    def adjust_buttons(self):
        pass
