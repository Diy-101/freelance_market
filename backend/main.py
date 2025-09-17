from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.bot import start_telegram
from src.database import init_models
from src.user_service.api.users import user_router
from src.utils.logger import logger
from src.webhook import webhook_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Start Application!!!")
    await start_telegram()
    await init_models()
    yield
    logger.info("⛔ Stop Application")


app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://freelance-market-chi.vercel.app",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )
