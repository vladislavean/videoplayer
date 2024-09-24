from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class PostgreSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ASYNC_SESSIONMAKER_OBJECT(self):
        engine = create_async_engine(postgre_settings.DATABASE_URL)
        return async_sessionmaker(engine, expire_on_commit=False)

    model_config = SettingsConfigDict(env_file=".env")


postgre_settings = PostgreSettings()
