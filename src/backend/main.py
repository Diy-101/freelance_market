from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.utils.logger import logger
from src.bot import start_telegram
from src.webhook import telegram_router

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Start Application!!!")
    await start_telegram()
    yield
    logger.info("⛔ Stop Application")

app = FastAPI(lifespan=lifespan)
app.include_router(telegram_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000)