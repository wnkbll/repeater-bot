from pydantic import BaseModel, FilePath, AnyUrl


class Post(BaseModel):
    text: str
    file: FilePath | None = None


class Chat(BaseModel):
    url: AnyUrl
    time: list[str] | int
