from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class BookSchema(BaseModel):
    id: int
    title: str
    year: int
    id_novelist: int


class BookUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    id_novelist: int | None = None


class BookList(BaseModel):
    books: list[BookSchema]


class NovelistSchema(BaseModel):
    name: str


class NovelistAllInfoSchema(BaseModel):
    name: str
    id: int


class NoveLists(BaseModel):
    novelists: list[NovelistAllInfoSchema]


class UserBooksRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    read_books: list[BookSchema]

    model_config = ConfigDict(from_attributes=True)
