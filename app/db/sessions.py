from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.tables.profiles import Profile

engine = create_engine(
    settings.sync_database_url,
    echo=settings.db_echo_log,
)

async_engine = create_async_engine(
    settings.async_database_url,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_and_tables() -> None:
    '''Verifica se o banco de dados existe,
    caso não exista, cria-o'''
    if not database_exists(engine.url):
        create_database(engine.url)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


async def reset_tables() -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


async def bulk_create_profiles(number: int) -> None:
    fake = Faker()
    async with AsyncSession(async_engine) as session:
        for _ in range(number):
            profile = Profile(**fake.profile())
            session.add(profile)

        await session.commit()
