from contextlib import asynccontextmanager
from typing import AsyncGenerator

from api_analytics.fastapi import Analytics
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.repositories.task import TaskRepository
from api.rmq import AsyncRabbitMQProducer
from api.services.task import TaskService
from database import init_db
from logger import logger
from routers.user import router as user_router
from routers.task import router as task_router
from settings import settings
from starlette.types import Lifespan

from api.repositories.user import UserRepository
from api.services.user import UserService


def create_app(lifespan: Lifespan) -> FastAPI:
    """
    Create and configure an instance of the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version="dev",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.include_router(prefix="/api/v1", router=user_router)
    app.include_router(prefix="/api/v1", router=task_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(Analytics, api_key=settings.ANALYTICS_API_KEY)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("App startup...")
    # set_up_logger()
    await init_db()

    producer = AsyncRabbitMQProducer()
    app.state.user_service = UserService(repo_factory=lambda session: UserRepository(session))
    app.state.task_service = TaskService(
        repo_factory=lambda session: TaskRepository(session), producer=producer
    )
    yield
    logger.info("App shutdown.")


app = create_app(lifespan=lifespan)
