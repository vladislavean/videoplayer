from app.database.settings import postgre_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.exceptions import catch_db_errors
from sqlalchemy import select, insert, update, delete


engine = create_async_engine(postgre_settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@catch_db_errors
async def select_all(model):
    async with async_session_maker() as session:
        query = select(model.__table__.columns)
        result = await session.execute(query)
        return result.mappings().all()


@catch_db_errors
async def find_one_or_none(model, **filter_by):
    async with async_session_maker() as session:
        query = select(model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()


@catch_db_errors
async def find_all(model, **filter_by):
    async with async_session_maker() as session:
        query = select(model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()


@catch_db_errors
async def insert_one(model, **data):
    async with async_session_maker() as session:
        query = insert(model).values(**data).returning()
        await session.execute(query)
        await session.commit()
        return {'status': 'OK'}
