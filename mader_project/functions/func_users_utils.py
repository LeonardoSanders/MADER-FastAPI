from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from mader_project.models import User
from mader_project.schemas import UserSchema


# Users Util Fuctions
async def verify_existing_user_by_name_and_email(
    user: UserSchema, session: AsyncSession
):
    user_db = await session.scalar(
        select(User).where(
            (User.name == user.name) | (User.email == user.email)
        )
    )

    if user_db:
        if user_db.name == user.name:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists!',
            )
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists!'
        )


async def verify_existing_user_by_id(user_id: int, session: AsyncSession):
    user_db = await session.scalar(
        select(User)
        .where(User.id == user_id, User.status)
        .options(selectinload(User.read_books))
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    return user_db


def verify_similar_user_id(c_user_id: int, user_id: int):
    if c_user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission!'
        )
