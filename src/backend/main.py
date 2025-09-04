from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.bot import start_telegram
from src.database import init_models
from src.presentation.fastapi_routers.orders import order_router
from src.presentation.fastapi_routers.users import user_router
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
app.include_router(order_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="debug",
    )
