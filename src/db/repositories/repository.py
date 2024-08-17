from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class Repository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory: async_sessionmaker[AsyncSession] = session_factory

    async def create(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    async def get(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    async def get_all(self, **kwargs) -> list[BaseModel]:
        raise NotImplementedError

    async def update(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    async def delete(self, **kwargs) -> BaseModel:
        raise NotImplementedError
