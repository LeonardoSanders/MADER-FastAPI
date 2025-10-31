from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy import select

from mader_project.dependencies import CurrentUser, Session
from mader_project.functions.func_novelists_utils import (
    verify_existing_novelist_by_id,
    verify_existing_novelist_by_name,
)
from mader_project.functions.normalize_text import normalize_text
from mader_project.models import Novelist
from mader_project.schemas import Message, NoveLists, NovelistSchema

router = APIRouter(prefix='/novelists', tags=['novelists'])


@router.post(
    '/create-novelist',
    status_code=HTTPStatus.CREATED,
    response_model=NovelistSchema,
)
async def create_novelist(
    novelist: NovelistSchema, session: Session, current_user: CurrentUser
):
    await verify_existing_novelist_by_name(novelist.name, session)

    novelist_name = normalize_text(novelist.name)

    new_novelist = Novelist(name=novelist_name)

    session.add(new_novelist)
    await session.commit()
    await session.refresh(new_novelist)

    return new_novelist


@router.get(
    '/list-novelists', response_model=NoveLists, status_code=HTTPStatus.OK
)
async def get_all_novelists(session: Session, current_user: CurrentUser):
    novelists_db = (await session.scalars(select(Novelist))).all()
    return {'novelists': novelists_db}


@router.get(
    '/list-novelists/{name}',
    status_code=HTTPStatus.OK,
    response_model=NoveLists,
)
async def get_novelists_by_filter_name(
    name: str, session: Session, current_user: CurrentUser
):
    query = select(Novelist).where(Novelist.name.ilike(f'%{name}%'))

    novelists_db = (await session.scalars((query))).all()
    return {'novelists': novelists_db}


@router.get(
    '/novelist/{id}', response_model=NovelistSchema, status_code=HTTPStatus.OK
)
async def get_novelist_by_id(
    id: int, session: Session, current_user: CurrentUser
):
    novelist_db = await verify_existing_novelist_by_id(id, session)

    return novelist_db


@router.put(
    '/edit-novelist/{id}',
    response_model=NovelistSchema,
    status_code=HTTPStatus.OK,
)
async def edit_novelist_by_id(
    id: int,
    novelist: NovelistSchema,
    session: Session,
    current_user: CurrentUser,
):
    novelist_db = await verify_existing_novelist_by_id(id, session)
    novelist_name = normalize_text(novelist.name)
    await verify_existing_novelist_by_name(novelist.name, session)

    novelist_db.name = novelist_name

    await session.commit()
    await session.refresh(novelist_db)

    return novelist_db


@router.delete(
    '/delete-novelist/{id}', response_model=Message, status_code=HTTPStatus.OK
)
async def delete_novelist_by_id(
    id: int,
    session: Session,
    current_user: CurrentUser,
):
    novelist_db = await verify_existing_novelist_by_id(id, session)

    await session.delete(novelist_db)
    await session.commit()

    return {'message': 'Novelist deleted!'}
