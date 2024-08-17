from sqlalchemy import select, update, delete, Executable

from src.db.errors import EntityDoesNotExistError
from src.db.repositories.repository import Repository
from src.db.tables import PostsTable
from src.models.posts import Post, PostInCreate, PostInUpdate


class PostsRepository(Repository):
    async def create(self, *, post_in_create: PostInCreate) -> Post:
        post_row = PostsTable(text=post_in_create.text, file=post_in_create.file)

        async with self.session_factory() as session:
            session.add(post_row)
            await session.commit()

        return Post.model_validate(post_row, from_attributes=True)

    async def get(self, *, id_: int) -> Post:
        query: Executable = select(PostsTable).filter_by(id=id_)

        async with self.session_factory() as session:
            response = await session.execute(query)

            post_row = response.scalars().first()
            if post_row is None:
                raise EntityDoesNotExistError(f"Post with id:{id_} does not exist")

            return Post.model_validate(post_row, from_attributes=True)

    async def get_all(self) -> list[Post]:
        query: Executable = select(PostsTable)

        async with self.session_factory() as session:
            response = await session.execute(query)
            posts = response.scalars().all()

            if posts is None:
                raise EntityDoesNotExistError("List of users is empty")

            return [
                Post.model_validate(post, from_attributes=True) for post in posts
            ]

    async def update(self, *, id_: int, post_in_update: PostInUpdate) -> Post:
        post_to_update = await self.get(id_=id_)

        post_to_update.text = post_in_update.text or post_to_update.text
        post_to_update.file = post_in_update.file or post_to_update.file

        query: Executable = (
            update(PostsTable).
            values(
                text=post_to_update.text,
                file=post_to_update.file,
            ).
            filter_by(id=id_)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return post_to_update

    async def delete(self, *, id_: int) -> Post:
        post = await self.get(id_=id_)

        query: Executable = delete(PostsTable).filter_by(id=id_)

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return post
