from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy import select

from mader_project.models import User
from mader_project.schemas import UserSchema
from mader_project.dependencies import Session


async def verify_existing_user(user: UserSchema, session: Session):
    user_db = await session.scalar(
        select(User).where(
            (User.name == user.name) | (User.email == user.email)
        ))
    
    if user_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User already exists!'
        )
