from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from mader_project.dependencies import CurrentUser, OAuthForm, Session
from mader_project.models import User
from mader_project.schemas import Token
from mader_project.security import create_acess_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token, status_code=HTTPStatus.CREATED)
async def login_for_access_token(form_data: OAuthForm, session: Session):
    user_db = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect Email or Password!',
        )

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect Email or Passoword',
        )

    access_token = create_acess_token(data={'sub': user_db.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post(
    '/refresh_access_token',
    response_model=Token,
    status_code=HTTPStatus.CREATED,
)
async def refresh_token(user: CurrentUser):
    new_access_token = create_acess_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
