from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from mader_project.dependencies import CurrentUser, Session
from mader_project.functions.func_books_utils import verify_existing_book_by_id
from mader_project.functions.func_users_utils import (
    verify_existing_user_by_id,
    verify_existing_user_by_name_and_email,
    verify_similar_user_id,
)
from mader_project.models import User
from mader_project.schemas import (
    Message,
    UserList,
    UserPublic,
    UserPublicBooks,
    UserSchema,
)
from mader_project.security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
async def create_user(user: UserSchema, session: Session):
    await verify_existing_user_by_name_and_email(user, session)

    user_db = User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db


@router.get(
    '/list-all-users', response_model=UserList, status_code=HTTPStatus.OK
)
async def list_all_users(session: Session, current_user: CurrentUser):
    users_db = (
        await session.scalars(
            select(User)
            .where(User.status)
            .options(selectinload(User.read_books))
        )
    ).all()

    return {'users': users_db}


@router.get(
    '/user/{user_id}',
    response_model=UserPublicBooks,
    status_code=HTTPStatus.OK,
)
async def get_user_by_id(
    user_id: int, session: Session, current_user: CurrentUser
):
    user_db = await verify_existing_user_by_id(user_id, session)

    return user_db


@router.put(
    '/user-to-edit/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    summary='Endpoint para edição de usuários',
)
async def edit_user_by_id(
    user_id: int, user: UserSchema, session: Session, current_user: CurrentUser
):
    await verify_existing_user_by_id(user_id, session)

    verify_similar_user_id(current_user.id, user_id)

    try:
        current_user.name = user.name
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists!',
        )


@router.delete(
    '/delete_user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    summary='Endpoint to delete users',
)
async def delete_user_by_id(
    user_id: int, session: Session, current_user: CurrentUser
):
    await verify_existing_user_by_id(user_id, session)

    verify_similar_user_id(current_user.id, user_id)

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted!'}


# Endpoint para relacionar Livros lidos por Usuário
@router.post(
    '/books-read/{book_id}',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
async def books_read_by_user(
    book_id: int, session: Session, current_user: CurrentUser
):
    book_db = await verify_existing_book_by_id(book_id, session)

    if book_db not in current_user.read_books:
        current_user.read_books.append(book_db)

        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

    return {'message': 'Book added to the user book list!'}
