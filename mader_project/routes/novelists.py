from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from mader_project.dependencies import Session, CurrentUser
from mader_project.schemas import NovelistSchema, NoveLists, Message
from mader_project.models import Novelist

from mader_project.functions.func_novelists_utils import (
    verify_existing_novelist_by_name,
    verify_existing_novelist_by_id
)

router = APIRouter(prefix='/novelists', tags=['novelists'])


@router.post(
    '/create-novelist',
    response_model=NovelistSchema,
    status_code=HTTPStatus.CREATED
)
async def create_novelist(
    novelist: NovelistSchema,
    session: Session,
    current_user: CurrentUser
):
    await verify_existing_novelist_by_name(novelist.name, session)

    new_novelist = Novelist(
        name=novelist.name
    )

    session.add(new_novelist)
    await session.commit()
    await session.refresh(new_novelist)

    return new_novelist


@router.get(
    '/list-novelists',
    response_model=NoveLists,
    status_code=HTTPStatus.OK
)
async def get_all_novelists(session: Session, current_user: CurrentUser):
    novelists_db = (await session.scalars(select(Novelist))).all()
    return {'novelists': novelists_db}


@router.get(
    '/list-novelists/{name}',
    response_model=NoveLists,
    status_code=HTTPStatus.OK
)
async def get_novelists_by_filter_name(
    name: str,
    session: Session,
    current_user: CurrentUser
):
    query = select(Novelist).where(Novelist.name.ilike(f'%{name}%'))

    novelists_db = (await session.scalars((query))).all()
    return {'novelists': novelists_db}


@router.get(
    '/novelist/{id}',
    response_model=NovelistSchema,
    status_code=HTTPStatus.OK
)
async def get_novelist_by_id(
    novel_id: int,
    session: Session,
    current_user: CurrentUser
):
    novelist_db = await verify_existing_novelist_by_id(novel_id, session)
    
    return novelist_db


@router.put(
    '/edit-novelist/{id}',
    response_model=NovelistSchema,
    status_code=HTTPStatus.OK,
)
async def edit_novelist_by_id(
    novel_id: int,
    novelist: NovelistSchema,
    session: Session,
    current_user: CurrentUser
):
    novelist_db = await verify_existing_novelist_by_id(novel_id, session)

    try:
        novelist_db.name = novelist.name

        await session.commit()
        await session.refresh(novelist_db)

        return novelist_db
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Novelist already exists!'
        )
    

@router.delete(
    '/delete-novelist/{id}',
    response_model=Message,
    status_code=HTTPStatus.OK
)
async def delete_novelist_by_id(
    novel_id: int,
    session: Session,
    current_user: CurrentUser,
):
    novelist_db = await verify_existing_novelist_by_id(novel_id, session)
    
    try:
        await session.delete(novelist_db)
        await session.commit()

        return {'message': 'Novelist deleted from MADER database'}
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Novelist already deleted!'
        )