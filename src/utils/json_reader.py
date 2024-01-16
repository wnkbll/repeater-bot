import os
import json
import inspect

from loguru import logger
from typing import Any

PathLike = str | os.PathLike

ModuleName = str
FuncName = str
Caller = tuple[ModuleName, FuncName]


class JsonReader:
    @staticmethod
    def write(obj: Any, path: PathLike, debug: bool = True, caller: Caller = ("none", "none")) -> None:
        folder, _ = os.path.split(path)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(path, mode="w", encoding="utf-8") as json_file:
            json.dump(obj, json_file, indent=4)

        if debug:
            line = inspect.currentframe().f_back.f_lineno
            logger.debug(f"File {path} has been written in {caller[0]}:{caller[1]}:{line}.")

    @staticmethod
    def read(path: PathLike, debug: bool = True, caller: Caller = ("none", "none")) -> Any:
        if not os.path.exists(path):
            return []

        with open(path, encoding="utf-8") as json_file:
            file = json.load(json_file)

        if debug:
            line = inspect.currentframe().f_back.f_lineno
            logger.debug(f"File {path} has been read in {caller[0]}:{caller[1]}:{line}.")

        return file
