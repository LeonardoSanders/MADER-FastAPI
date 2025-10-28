from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader_project.models import Book


async def verify_existing_book_by_id(book_id: int, session: AsyncSession):
    book_db = await session.get(Book, book_id)

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found!'
        )
    
    return book_db


async def verify_existing_book_by_title(
    book_title: str, session: AsyncSession):

    book_db = await session.scalar(
        select(Book).where(Book.title == book_title))
    
    if book_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Book already exists!'
        )