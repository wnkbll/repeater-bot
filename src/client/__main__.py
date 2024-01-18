import time
import schedule

from telethon import TelegramClient, errors
from telethon.hints import EntityLike

from loguru import logger

from src.utils import environment, Config, JsonReader, TimeSetter, Dictionaries
from src.lang import STRINGS

lang = "ru"

config_path = "data/config.json"
data_path = "data/data.json"


class Client:
    def __init__(self):
        self.client = TelegramClient("session/client", environment.api_id, environment.api_hash, system_version="4.16.30-vxCUSTOM")
        self.client.start(environment.phone)
        self.client.disconnect()

        self.config = Config(**JsonReader.read(config_path, True, ("src.bot", "__init__")))
        self.chats = self.config.chats
        self.start, self.stop = TimeSetter.get_interval(self.config.sleep)

        self.indexes: dict[str, int] = {}
        for key in self.chats.keys():
            self.indexes[key] = 0

        self.is_scheduled = False

    async def repeat(self, chat: EntityLike):
        posts = JsonReader.read(data_path, False)

        if len(posts) <= 0:
            return

        try:
            entity = await self.client.get_entity(chat)
        except ValueError:
            logger.error(STRINGS["debug"]["entity_existence_error"].format(chat=chat))
            return

        index = self.indexes[chat]
        if index >= len(posts):
            index = 0
            self.indexes[chat] = 1
        else:
            self.indexes[chat] = index + 1

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

    def setup(self, chat: EntityLike) -> None:
        self.client.start(environment.phone)
        self.client.loop.run_until_complete(self.repeat(chat))
        self.client.disconnect()

    def set_schedule(self) -> None:
        for chat in self.chats.items():
            if isinstance(chat[1], list):
                for _time in chat[1]:
                    schedule.every().day.at(TimeSetter.localize(_time)).do(self.setup, chat=chat[0])
            else:
                schedule.every(chat[1]).minutes.do(self.setup, chat=chat[0])

    def update_indexes(self, _config) -> None:
        added, deleted = Dictionaries.compare_dictionaries(self.chats, _config.chats)
        for key in added:
            self.indexes[key] = 0
        for key in deleted:
            self.indexes.pop(key)

    def update_config(self) -> None:
        _config = Config(**JsonReader.read(config_path, False))

        if self.config != _config:
            logger.info(STRINGS["debug"]["config_changed"])

            self.update_indexes(_config)

            self.config = _config
            self.chats = self.config.chats
            self.start, self.stop = TimeSetter.get_interval(self.config.sleep)

            schedule.clear()
            self.is_scheduled = False

    def main(self) -> None:
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


if __name__ == '__main__':
    Client().main()
