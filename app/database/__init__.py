from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from app.database.settings import postgre_settings


engine = create_async_engine(postgre_settings.DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



