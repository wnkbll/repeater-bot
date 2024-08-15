from pydantic import FilePath

from src.models import Post


class PostsService:
    def __init__(self):
        self.posts: list[Post] = []

    async def create(self, text: str, file: FilePath = None) -> None:
        post = Post(text=text) if file is None else Post(text=text, file=file)
        self.posts.append(post)

    async def get(self) -> None:
        pass

    async def update(self) -> None:
        pass

    async def delete(self) -> None:
        pass
