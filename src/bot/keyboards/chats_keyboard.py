from aiogram.types import InlineKeyboardButton

from src.bot.keyboards import Keyboard
from src.bot.callbacks import ChatsCallback


class ChatsKeyboard(Keyboard):
    def __init__(self, amount_of_buttons: int, action: str, chats: dict[str, int | list[str]]):
        super().__init__(amount_of_buttons, action)
        self.chats = chats

        self.add_buttons()
        self.adjust_buttons()

    def add_buttons(self):
        for index, item in enumerate(self.chats.items()):  # TODO Нельзя пихать ссылку в ChatsCallback?
            self.builder.add(InlineKeyboardButton(text=f"{index + 1}", callback_data=ChatsCallback(action=self.action, chat=item[0]).pack()))

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
