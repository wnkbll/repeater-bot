from pydantic import TypeAdapter

from src.core.settings import settings
from src.db.postgres import Postgres
from src.db.redis import Redis
from src.db.repositories.posts import PostsRepository
from src.models.posts import Post, PostInCreate, PostInUpdate


class PostsService:
    def __init__(self):
        async_session_factory = Postgres.get_async_session_factory()
        self.posts_repo = PostsRepository(async_session_factory)
        self.type_adapter = TypeAdapter(Post)

    async def cache_post(self, post: Post) -> None:
        key = f"{settings.prefixes.posts}:{post.id}"
        encoded = self.type_adapter.dump_json(post).decode("utf-8")
        await Redis.set(key=key, value=encoded)

    async def create(self, *, text: str, file: str = None) -> Post:
        post_in_create = PostInCreate(text=text, file=file)
        post = await self.posts_repo.create(post_in_create=post_in_create)

        await self.cache_post(post)

        return post

    async def get(self, *, id_: int) -> Post:
        key = f"{settings.prefixes.posts}:{id_}"
        encoded = await Redis.get(key=key)

        if encoded is not None:
            return self.type_adapter.validate_json(encoded)

        return await self.posts_repo.get(id_=id_)

    async def update(self, *, id_: int, text: str = None, file: str = None) -> Post:
        post_in_update = PostInUpdate(text=text, file=file)
        post = await self.posts_repo.update(id_=id_, post_in_update=post_in_update)

        await self.cache_post(post)

        return post

    async def delete(self, *, id_: int) -> Post:
        key = f"{settings.prefixes.posts}:{id_}"
        if await Redis.exists(key=key):
            await Redis.delete(key=key)

        return await self.posts_repo.delete(id_=id_)
