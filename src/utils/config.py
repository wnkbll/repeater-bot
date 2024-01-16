import os

from src.utils.json_reader import JsonReader

PathLike = str | os.PathLike


class ConfigSchema:
    white_list: list[int]
    chats: dict[str, int | list[str]]
    sleep: dict[str, str | bool]


class Config(ConfigSchema):
    def __init__(self, path: PathLike):
        config = JsonReader.read(path, False)

        self.white_list = config["white_list"]
        self.chats = config["chats"]
        self.sleep = config["sleep"]
