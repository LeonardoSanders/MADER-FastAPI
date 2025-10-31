from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from factory import Factory, LazyAttribute, Sequence  # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import selectinload
from testcontainers.postgres import PostgresContainer

from mader_project.app import app
from mader_project.database import get_session
from mader_project.models import Book, Novelist, User, table_registry
from mader_project.security import get_password_hash
from mader_project.settings import Settings


@pytest.fixture
def settings():
    return Settings()  # type: ignore


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(model, time=datetime(2025, 10, 29)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
            if hasattr(target, 'updated_at'):
                target.updated_at = time

    event.listen(User, 'before_insert', fake_time_hook)
    event.listen(Novelist, 'before_insert', fake_time_hook)
    event.listen(Book, 'before_insert', fake_time_hook)

    yield time

    event.remove(User, 'before_insert', fake_time_hook)
    event.remove(Novelist, 'before_insert', fake_time_hook)
    event.remove(Book, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    new_user = UserFactory()
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    user = await session.scalar(
        select(User)
        .where(User.id == new_user.id)
        .options(selectinload(User.read_books))
    )
    assert user is not None  # Ensure user is found

    new_user.clean_password = f'{user.name}@example.com'

    return user


@pytest_asyncio.fixture
async def other_user(session: AsyncSession):
    user = UserFactory()

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = f'{user.name}@example.com'

    return user


@pytest_asyncio.fixture
async def novelist(session: AsyncSession):
    novelist = NovelistFactory()

    session.add(novelist)
    await session.commit()
    await session.refresh(novelist)

    return novelist


@pytest_asyncio.fixture
async def book(session: AsyncSession, novelist: Novelist):
    book = BookFactory(id_novelist=novelist.id)

    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


class UserFactory(Factory):
    class Meta:
        model = User

    name = Sequence(lambda n: f'test{n}')
    email = LazyAttribute(lambda obj: f'{obj.name}@test.com')
    password = LazyAttribute(
        lambda obj: get_password_hash(f'{obj.name}@example.com')
    )


class NovelistFactory(Factory):
    class Meta:
        model = Novelist

    name = Sequence(lambda n: f'Escritor {n}')


class BookFactory(Factory):
    class Meta:
        model = Book

    id_novelist = Sequence(lambda n: n + 1)
    title = Sequence(lambda n: f'Book {n}')
    year = Sequence(lambda n: f'{19}{n}{n}')
