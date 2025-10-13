from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from mader_project.database import AsyncSession, get_session
from mader_project.dependencies import Session
from mader_project.models import User
from mader_project.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema
)


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/registrer', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserPublic, session: Session):
    ...