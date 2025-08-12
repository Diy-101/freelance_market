from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.utils.logger import logger
from src.bot import start_telegram
from src.webhook import webhook_router
from src.auth import authx
from src.auth.routers import user_router
from src.utils.database import Base, engine
from src.auth.models import User

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Start Application!!!")
    await start_telegram()
    yield
    logger.info("⛔ Stop Application")

app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
authx.handle_errors(app)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000)