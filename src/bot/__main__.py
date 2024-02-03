import asyncio

from aiogram import Bot, Dispatcher

from loguru import logger

from src.bot.routes import routers

from src.utils import environment
from src.lang import STRINGS


async def setup():
    bot = Bot(token=environment.token)
    dp = Dispatcher()

    logger.success(STRINGS["debug"]["connected"].format(bot="Bot"))

    for router in routers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    asyncio.run(setup())


if __name__ == "__main__":
    main()
