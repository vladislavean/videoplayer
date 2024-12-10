from fastapi import FastAPI

from app.database.redis_settings import redis
from app.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    try:
        await redis.ping()
        print("Redis connection established")
    except Exception as e:
        print(f"Redis connection failed: {e}")


@app.on_event("shutdown")
async def shutdown():
    await redis.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
