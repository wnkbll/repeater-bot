import os

from src.utils.json_reader import JsonReader

PathLike = str | os.PathLike


class ConfigSchema:
    white_list: list[int]
    chats: dict[str, int | list[str]]
    sleep: dict[str, str | bool]


class Config(ConfigSchema):
    def __init__(self, path: PathLike):
        _config = JsonReader.read(path, False)

        self.white_list = _config["white_list"]
        self.chats = _config["chats"]
        self.sleep = _config["sleep"]


config = Config("data/config.json")
