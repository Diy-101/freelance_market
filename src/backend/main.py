from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from bot import start_telegram


@asynccontextmanager
async def lifespan(application: FastAPI):
    logging.info("Start Application!!!")
    await start_telegram()
    yield
    logging.info("⛔ Stop Application")

app = FastAPI(lifespan=lifespan)
