from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.redis_settings import redis
from app.routers.archives import archives_router
from app.routers.cameras import cameras_router
from app.routers.streets import streets_router
from app.routers.users import users_router
from app.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await redis.ping()
        print("Redis connection established")
    except Exception as e:
        print(f"Redis connection failed: {e}")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(archives_router)
app.include_router(cameras_router)
app.include_router(streets_router)
app.include_router(users_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
