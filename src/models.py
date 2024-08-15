from pydantic import BaseModel, FilePath, AnyUrl


class Post(BaseModel):
    text: str
    file: FilePath | None = None


class ListOfPosts(BaseModel):
    posts: list[Post]


class Chat(BaseModel):
    url: AnyUrl
    time: list[str] | int


class ListOfChats(BaseModel):
    chats: list[Chat]
