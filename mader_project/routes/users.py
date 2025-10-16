from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from mader_project.database import AsyncSession, get_session
from mader_project.dependencies import Session
from mader_project.models import User
from mader_project.security import get_password_hash
from mader_project.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema
)
from mader_project.user_utils import verify_existing_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
async def create_user(user: UserSchema, session: Session):
    await verify_existing_user(user, session)

    try:
        user_db = User(
            name=user.name,
            email=user.email,
            password=get_password_hash(user.password),
        )

        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)
        
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )

    return user_db