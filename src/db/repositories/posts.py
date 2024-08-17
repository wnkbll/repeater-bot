from src.db.repositories.repository import Repository
from src.models.posts import PostInDB


class PostsRepository(Repository):
    async def create(self, *, text: str, file: str = None) -> PostInDB:
        pass

    async def get(self, *, id_: int) -> PostInDB:
        pass

    async def get_all(self) -> list[PostInDB]:
        pass

    async def update(self, *, id_: int) -> PostInDB:
        pass

    async def delete(self, *, id_: int) -> PostInDB:
        pass
