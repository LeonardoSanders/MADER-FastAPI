from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader_project.models import Novelist


async def verify_existing_novelist_by_name(
    novel_name: str, session: AsyncSession):
    
    noveslit_db = await session.scalar(
        select(Novelist).where(Novelist.name == novel_name))
    
    if noveslit_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Novelist already exists!'
        )
    

async def verify_existing_novelist_by_id(novel_id: int, session: AsyncSession):
    novelist_db = await session.get(Novelist, novel_id)

    if not novelist_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist not found!'
        )
    
    return novelist_db