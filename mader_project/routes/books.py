from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy import select

from mader_project.dependencies import CurrentUser, Session
from mader_project.functions.func_books_utils import (
    verify_existing_book_by_id,
    verify_existing_book_by_title,
)
from mader_project.functions.normalize_text import normalize_text
from mader_project.models import Book
from mader_project.schemas import (
    BookCreation,
    BookList,
    BookSchema,
    BookUpdate,
    Message,
)

router = APIRouter(prefix='/books', tags=['books'])


@router.post(
    '/create-book', status_code=HTTPStatus.CREATED, response_model=BookSchema
)
async def create_book(
    book: BookCreation, session: Session, current_user: CurrentUser
):
    await verify_existing_book_by_title(book.title, session)

    book_title = normalize_text(book.title)

    new_book = Book(
        title=book_title, year=book.year, id_novelist=book.id_novelist
    )

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


@router.get(
    '/list-all-books', response_model=BookList, status_code=HTTPStatus.OK
)
async def get_all_books(session: Session, current_user: CurrentUser):
    books_db = (await session.scalars(select(Book))).all()

    if not books_db:
        return {'books': []}

    return {'books': books_db}


@router.get(
    '/get-book/{book_id}', response_model=BookSchema, status_code=HTTPStatus.OK
)
async def get_book_by_id(
    book_id: int, session: Session, current_user: CurrentUser
):
    book_db = await verify_existing_book_by_id(book_id, session)

    return book_db


@router.get(
    '/list-book/{title}/{year}',
    status_code=HTTPStatus.OK,
    response_model=BookList,
)
async def list_books_by_year(
    title: str, year: int, session: Session, current_user: CurrentUser
):
    query = (
        select(Book)
        .where(Book.title.ilike(f'%{title}%'))
        .where(Book.year == year)
    )

    books_filtered = (await session.scalars(query)).all()

    if not books_filtered:
        return {'books': []}

    return {'books': books_filtered}


@router.delete(
    '/delete-book/{book_id}', response_model=Message, status_code=HTTPStatus.OK
)
async def delete_book_by_id(
    book_id: int, session: Session, current_user: CurrentUser
):
    book_db = await verify_existing_book_by_id(book_id, session)

    await session.delete(book_db)
    await session.commit()

    return {'message': 'Book deleted!'}


@router.patch(
    '/update-book/{book_id}',
    status_code=HTTPStatus.OK,
    response_model=BookSchema,
)
async def update_book(
    book_id: int,
    session: Session,
    current_user: CurrentUser,
    book: BookUpdate,
):
    book_db = await verify_existing_book_by_id(book_id, session)

    for key, value in book.model_dump(exclude_unset=True).items():
        final_value = normalize_text(value) if key == 'title' else value
        setattr(book_db, key, final_value)

    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)

    return book_db
