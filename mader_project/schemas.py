from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BookSchema(BaseModel):
    id: int
    id_novelist: int
    title: str
    year: int

    model_config = ConfigDict(from_attributes=True)


class BookCreation(BaseModel):
    id_novelist: int
    title: str
    year: int


class BookUpdate(BaseModel):
    id_novelist: int | None = None
    title: str | None = None
    year: int | None = None


class BookList(BaseModel):
    books: list[BookSchema]


class NovelistSchema(BaseModel):
    name: str


class NovelistAllInfoSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NoveLists(BaseModel):
    novelists: list[NovelistAllInfoSchema]


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserPublicBooks(BaseModel):
    id: int
    name: str
    email: EmailStr
    read_books: list[BookSchema]

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublicBooks]
