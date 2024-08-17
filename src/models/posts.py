from pydantic import BaseModel, FilePath

from src.models.base import IDModelMixin, TimestampsModelMixin


class PostInDB(IDModelMixin, TimestampsModelMixin):
    text: str
    file: FilePath | None = None


class PostInCreate(BaseModel):
    text: str
    file: FilePath | None = None


class PostInUpdate(BaseModel):
    text: str | None = None
    file: FilePath | None = None


class ListOfPosts(BaseModel):
    posts: list[PostInDB]
