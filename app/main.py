from fastapi import FastAPI
from app.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(api_router)
origins = [

    "http://10.8.0.6:3000/videoCamers",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.8.0.1", port=8000)