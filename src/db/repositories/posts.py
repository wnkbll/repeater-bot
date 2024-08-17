from src.db.repositories.repository import Repository
from src.models.posts import Post, PostInCreate, PostInUpdate


class PostsRepository(Repository):
    async def create(self, *, post_in_create: PostInCreate) -> Post:
        pass

    async def get(self, *, id_: int) -> Post:
        pass

    async def get_all(self) -> list[Post]:
        pass

    async def update(self, *, id_: int, post_in_update: PostInUpdate) -> Post:
        pass

    async def delete(self, *, id_: int) -> Post:
        pass
