from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.settings import settings
from src.db.tables import Table


class Postgres:
    @staticmethod
    def get_async_engine() -> AsyncEngine | None:
        try:
            async_engine: AsyncEngine = create_async_engine(settings.postgres_dsn)
            return async_engine
        except SQLAlchemyError as e:
            logger.warning("Unable to establish db engine, database might not exist yet")

    @staticmethod
    async def initialize_database() -> None:
        async_engine = Postgres.get_async_engine()
        async with async_engine.begin() as async_conn:
            await async_conn.run_sync(Table.metadata.create_all)

            logger.success("Initializing database was successfully.")
