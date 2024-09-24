from sqlalchemy.exc import SQLAlchemyError
from asyncpg import PostgresError
from functools import wraps
from fastapi import HTTPException


def catch_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="SQLAlchemy error occurred: " + str(e))

        except ConnectionRefusedError as e:
            raise HTTPException(status_code=500, detail="Database connection failed. error occurred: " + str(e))

        except PostgresError as e:
            raise HTTPException(status_code=500, detail="asyncpg error occurred: " + str(e))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error occurred: {type(e)} {str(e)}")

    return wrapper
