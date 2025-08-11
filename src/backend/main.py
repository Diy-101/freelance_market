from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.utils.logger import logger
from src.bot import start_telegram
from src.webhook import webhook_router
from src.auth import authx

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Start Application!!!")
    await start_telegram()
    yield
    logger.info("⛔ Stop Application")

app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)

authx.handle_errors(app)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000)