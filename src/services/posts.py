from src.db.postgres import Postgres
from src.db.repositories.posts import PostsRepository
from src.models.posts import Post, PostInCreate, PostInUpdate


class PostsService:
    def __init__(self):
        async_session_factory = Postgres.get_async_session_factory()
        self.posts_repo = PostsRepository(async_session_factory)

    async def create_post(self, *, text: str, file: str = None) -> Post:
        post_in_create = PostInCreate(text=text, file=file)

        return await self.posts_repo.create(post_in_create=post_in_create)

    async def get_post(self, *, id_: int) -> Post:
        return await self.posts_repo.get(id_=id_)

    async def update_post(self, *, id_: int, text: str = None, file: str = None) -> Post:
        post_in_update = PostInUpdate(text=text, file=file)

        return await self.posts_repo.update(id_=id_, post_in_update=post_in_update)

    async def delete_post(self, *, id_: int) -> Post:
        return await self.posts_repo.delete(id_=id_)
