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


class Sleep(BaseModel):
    start: str
    stop: str


class Config(BaseModel):
    white_list: list[int]
    chats: ListOfChats
    sleep: Sleep
