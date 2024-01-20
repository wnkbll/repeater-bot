import os
import time
import schedule

from telethon import TelegramClient, errors
from telethon.hints import EntityLike

from loguru import logger

from src.utils import Config, JsonReader, TimeSetter, Dictionaries
from src.lang import STRINGS

PathLike = str | os.PathLike

lang = "ru"

logger.add("logs/client/errors.log", level="ERROR", format="{time:DD.MM.YYYY, HH:mm:ss} | {level} | {message}",
           rotation="1MB", compression="zip")


class Client:
    def __init__(self, api_id: int, api_hash: str, phone: str, config_path: PathLike, data_path: PathLike):
        self.client = TelegramClient("session/client", api_id, api_hash, system_version="4.16.30-vxCUSTOM")
        self.client.start(lambda: phone)
        self.client.disconnect()

        logger.success(STRINGS["debug"]["connected"].format(bot="Client"))

        self.phone = phone

        self.config_path = config_path
        self.data_path = data_path

        self.config = Config(**JsonReader.read(config_path, False))
        self.chats = self.config.chats
        self.start, self.stop = TimeSetter.get_interval(self.config.sleep)

        self.indexes: dict[str, int] = {}
        for key in self.chats.keys():
            self.indexes[key] = 0

        self.is_scheduled = False

    async def send_post(self, chat: EntityLike):
        posts = JsonReader.read(self.data_path, False)

        if len(posts) <= 0:
            return None

        try:
            entity = await self.client.get_entity(chat)
        except ValueError:
            logger.error(STRINGS["debug"]["entity_existence_error"].format(chat=chat))
            return None

        try:
            index = self.indexes[chat]
            if index >= len(posts):
                index = 0
                self.indexes[chat] = 1
            else:
                self.indexes[chat] = index + 1
        except KeyError:
            index = 0

        try:
            await self.client.send_message(entity, posts[index]["message"], file=posts[index]["file"])
            logger.success(STRINGS[lang]["post_sent"].format(title=entity.title))
        except errors.FloodWaitError as e:
            logger.error(STRINGS["debug"]["flood_wait_error"].format(seconds=e.seconds, title=entity.title))
        except errors.SlowModeWaitError as e:
            logger.error(STRINGS["debug"]["slow_mode_wait_error"].format(seconds=e.seconds, title=entity.title))
        except errors.ChannelPrivateError:
            logger.error(STRINGS["debug"]["channel_private_error"].format(title=entity.title))
        except errors.BadMessageError:
            logger.error(STRINGS["debug"]["bad_message_error"].format(title=entity.title))
        except KeyError as e:
            logger.error(STRINGS["debug"]["bad_message_error"].format(traceback=e.__traceback__))

    def setup(self, chat: EntityLike) -> None:
        self.client.start(lambda: self.phone)
        self.client.loop.run_until_complete(self.send_post(chat))
        self.client.disconnect()

    def set_schedule(self) -> None:
        for chat in self.chats.items():
            if isinstance(chat[1], list):
                for _time in chat[1]:
                    schedule.every().day.at(TimeSetter.localize(_time)).do(self.setup, chat=chat[0])
            else:
                schedule.every(chat[1]).minutes.do(self.setup, chat=chat[0])

    def update_indexes(self, _config: Config) -> None:
        added, deleted = Dictionaries.compare_dictionaries(self.chats, _config.chats)
        for key in added:
            self.indexes[key] = 0
        for key in deleted:
            self.indexes.pop(key)

    def update_config(self) -> None:
        _config = Config(**JsonReader.read(self.config_path, False))

        if self.config != _config:
            logger.info(STRINGS["debug"]["config_changed"])

            self.update_indexes(_config)

            self.config = _config
            self.chats = self.config.chats
            self.start, self.stop = TimeSetter.get_interval(self.config.sleep)

            schedule.clear()
            self.is_scheduled = False

    def run(self) -> None:
        while True:
            if TimeSetter.is_in_sleep(self.start, self.stop):
                schedule.clear()
                self.is_scheduled = False
            elif not self.is_scheduled:
                self.set_schedule()
                self.is_scheduled = True

            self.update_config()

            schedule.run_pending()
            time.sleep(1)
