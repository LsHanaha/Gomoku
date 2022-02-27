import pytest_asyncio
import asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from app.main import web_app
from app.models import Base, get_db, user_models
from app import AuthJWT


from app.config import settings


_base_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}" \
            f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database_testing}"
_engine = create_engine(_base_url)
_TestSessionLocal = sessionmaker(bind=_engine)


def override_db():

    try:
        db = _TestSessionLocal()
        yield db
    finally:
        db.close()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest_asyncio.fixture(scope="session")
async def test_application(event_loop):
    Base.metadata.create_all(bind=_engine)
    web_app.dependency_overrides[get_db] = override_db

    async with AsyncClient(app=web_app, base_url="http://testserver") as test_client:
        yield test_client
    Base.metadata.drop_all(bind=_engine)


@pytest_asyncio.fixture()
def authorization_fixture():
    return AuthJWT()


@pytest_asyncio.fixture()
async def app_with_game_tables(test_application):

    database_gen = override_db()

    db = next(database_gen)
    difficulties = [user_models.DifficultyLevel(name='Трус', algorithm_depth=1),
                    user_models.DifficultyLevel(name='Балбес', algorithm_depth=2),
                    user_models.DifficultyLevel(name='Бывалый', algorithm_depth=3),
                    user_models.DifficultyLevel(name='Джон Уие', algorithm_depth=4)
                    ]
    db.bulk_save_objects(difficulties)

    algorithms = [user_models.GomokuAlgorithm(name='min-max'), user_models.GomokuAlgorithm(name='wdwqdwf')]
    db.bulk_save_objects(algorithms)

    rules = [user_models.Rule(name='no rules', description='text'),
             user_models.Rule(name='Choice of redaction', description='text'),
             user_models.Rule(name='Karo', description='text')]
    db.bulk_save_objects(rules)

    db.commit()
    yield test_application


@pytest_asyncio.fixture()
async def create_user():
    db: Session = next(override_db())
    db.add(user_models.User(
        username='test_user',
        email="email@email.com",
        password="password"
    ))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
