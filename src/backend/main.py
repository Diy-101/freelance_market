from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from bot import start_telegram
from routers import telegram_router

@asynccontextmanager
async def lifespan(application: FastAPI):
    logging.info("Start Application!!!")
    await start_telegram()
    yield
    logging.info("⛔ Stop Application")

app = FastAPI(lifespan=lifespan)
app.include_router(telegram_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000)