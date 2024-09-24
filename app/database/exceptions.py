from sqlalchemy.exc import SQLAlchemyError
from asyncpg import PostgresError, CannotConnectNowError
from functools import wraps
from fastapi import HTTPException


def catch_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Выполнение основной функции
            return await func(*args, **kwargs)

        # Ловим исключения SQLAlchemy
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="SQLAlchemy error occurred: " + str(e))

        except CannotConnectNowError as e:
            raise HTTPException(status_code=500, detail="Database connection failed. error occurred: " + str(e))

        # Ловим исключения asyncpg (PostgreSQL)
        except PostgresError as e:
            raise HTTPException(status_code=500, detail="asyncpg error occurred: " + str(e))

        # Ловим любые другие ошибки
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error occurred: " + str(e))

    return wrapper
