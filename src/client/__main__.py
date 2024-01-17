import time
import random
import schedule

from telethon import TelegramClient, errors
from telethon.hints import EntityLike

from loguru import logger

from src.lang import STRINGS
from src.utils import environment, Config, JsonReader, TimeSetter

lang = "ru"


config_path = "data/config.json"
data_path = "data/data.json"


async def repeat(client: TelegramClient, chat: EntityLike) -> None:
    posts = JsonReader.read(data_path)

    if len(posts) <= 0:
        return

    try:
        entity = await client.get_entity(chat)
    except ValueError:
        logger.error(STRINGS[lang]["entity_existence_error"].format(chat=chat))
        return

    index = random.randint(0, len(posts) - 1)
    try:
        await client.send_message(entity, posts[index]["message"], file=posts[index]["file"])
        logger.success(STRINGS[lang]["post_sent"].format(title=entity.title))
    except errors.FloodWaitError as e:
        logger.error(STRINGS[lang]["flood_wait_error"].format(seconds=e.seconds, title=entity.title))
    except errors.SlowModeWaitError as e:
        logger.error(STRINGS[lang]["slow_mode_wait_error"].format(seconds=e.seconds, title=entity.title))
    except errors.ChannelPrivateError:
        logger.error(STRINGS[lang]["channel_private_error"].format(title=entity.title))
    except errors.BadMessageError:
        logger.error(STRINGS[lang]["bad_message_error"].format(title=entity.title))


def setup(client: TelegramClient, chat: EntityLike) -> None:
    client.start(environment.phone)
    client.loop.run_until_complete(repeat(client, chat))
    client.disconnect()


def set_scheduler(client: TelegramClient) -> None:
    chats = Config(**JsonReader.read(config_path, True, ("src.bot", "set_scheduler"))).chats

    for chat in chats.items():
        if isinstance(chat[1], list):
            for _time in chat[1]:
                schedule.every().day.at(TimeSetter.localize(_time)).do(setup, client=client, chat=chat[0])
        else:
            schedule.every(chat[1]).minutes.do(setup, client=client, chat=chat[0])


def main():
    client = TelegramClient("client", environment.api_id, environment.api_hash, system_version="4.16.30-vxCUSTOM").start(environment.phone)
    client.disconnect()

    config = Config(**JsonReader.read(config_path, True, ("src.bot", "main")))
    start, stop = TimeSetter.get_interval(config.sleep)

    is_scheduled = False

    while True:
        if TimeSetter.is_in_sleep(start, stop):
            schedule.clear()
            is_scheduled = False
        elif not is_scheduled:
            set_scheduler(client)
            is_scheduled = True

        _config = Config(**JsonReader.read(config_path, False))
        if config != _config:
            logger.info(STRINGS[lang]["config_changed"])
            config = _config
            start, stop = TimeSetter.get_interval(config.sleep)
            schedule.clear()
            is_scheduled = False

        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
