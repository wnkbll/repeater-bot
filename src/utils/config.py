from pydantic import BaseModel


class Config(BaseModel):
    white_list: list[int]
    chats: dict[str, int | list[str]]
    sleep: dict[str, str]
