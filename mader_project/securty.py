from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import (  # type: ignore
    DecodeError,
    ExpiredSignatureError,
    decode,
    encode,
)
from pwdlib import PasswordHash  # type: ignore
from sqlalchemy import select

from mader_project.database import AsyncSession, get_session
from mader_project.models import User
from mader_project.settings import Settings

pwd_context = PasswordHash.recommended()
settings = Settings()  # type: ignore
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_acess_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encode_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    
    return encode_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_schema)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    
    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception
    
    return user