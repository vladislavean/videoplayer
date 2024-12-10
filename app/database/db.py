from contextlib import asynccontextmanager

from app.database.settings import api_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.exceptions import catch_db_errors
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


engine = create_async_engine(api_settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@catch_db_errors
async def select_all(session: AsyncSession, model):
    query = select(model.__table__.columns)
    result = await session.execute(query)
    return result.mappings().all()


@catch_db_errors
async def find_one_or_none(session: AsyncSession, model, **filter_by):
    query = select(model.__table__.columns).filter_by(**filter_by)
    result = await session.execute(query)
    return result.mappings().one_or_none()


@catch_db_errors
async def find_all(session: AsyncSession, model, **filter_by):
    query = select(model.__table__.columns).filter_by(**filter_by)
    result = await session.execute(query)
    return result.mappings().all()


@catch_db_errors
async def insert_one(session: AsyncSession, model, **data):
    query = insert(model).values(**data).returning()
    result = await session.execute(query)
    await session.flush()
    return result.mappings().first()
