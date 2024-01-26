from aiogram.utils.keyboard import InlineKeyboardBuilder


class Keyboard:
    def __init__(self, amount_of_buttons: int, action: str):
        self.builder = InlineKeyboardBuilder()
        self.amount_of_buttons = amount_of_buttons
        self.action = action

    def add_buttons(self):
        pass

    def adjust_buttons(self):
        pass
