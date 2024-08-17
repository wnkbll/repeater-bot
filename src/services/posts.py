from src.db.postgres import Postgres
from src.db.repositories.posts import PostsRepository
from src.models.posts import PostInCreate


class PostsService:
    def __init__(self):
        async_session_factory = Postgres.get_async_session_factory()
        self.posts_repo = PostsRepository(async_session_factory)

    async def create_post(self, *, text: str, file: str = None) -> None:
        post_in_create = PostInCreate(text=text, file=file)

        await self.posts_repo.create(post_in_create=post_in_create)
