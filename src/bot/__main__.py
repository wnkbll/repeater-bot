import asyncio

from aiogram import Bot, Dispatcher

from loguru import logger

from src.bot.routes import routers

from src.utils import environment
from src.lang import STRINGS

lang = "ru"

logger.add("logs/bot/errors.log", level="ERROR", format="{time:DD.MM.YYYY, HH:mm:ss} | {level} | {message}",
           rotation="1MB", compression="zip")


async def setup():
    bot = Bot(token=environment.token)
    dp = Dispatcher()

    logger.success(STRINGS["debug"]["connected"])

    for router in routers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    asyncio.run(setup())


if __name__ == "__main__":
    main()
