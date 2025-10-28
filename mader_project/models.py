from datetime import datetime, date
from enum import Enum

from sqlalchemy import ForeignKey, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Read_Books_Association:
    __tablename__ = 'read_books_association'


    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id'), primary_key=True
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    status: Mapped[bool] = mapped_column(default=True)
    read_books: Mapped[list['Book']] = relationship(
        secondary='read_books_association',
        back_populates='read_by_users',
        init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Novelist:
    __tablename__ = 'novelists'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    books: Mapped[list['Book']] = relationship(
        init=False, back_populates='novelist'
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_novelist: Mapped[int] = mapped_column(ForeignKey('novelists.id'))
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int]
    novelist: Mapped[Novelist] = relationship(
        init=False, back_populates='books'
    )
    read_by_users: Mapped[list['User']] = relationship(
        secondary='read_books_association',
        back_populates='read_books',
        init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
