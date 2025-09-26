from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.analytics_service.api.analytics import analytics_router
from src.bot import start_telegram
from src.database import init_models
from src.notification_service.api.notifications import notification_router
from src.order_service.api.orders import order_router
from src.proposal_service.api.proposals import proposal_router
from src.search_service.api.search import search_router
from src.skill_service.api.skills import skill_router
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
app.include_router(order_router)
app.include_router(skill_router)
app.include_router(proposal_router)
app.include_router(notification_router)
app.include_router(search_router)
app.include_router(analytics_router)

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="debug",
    )
