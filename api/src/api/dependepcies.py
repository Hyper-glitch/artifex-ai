from database import async_session_maker
from fastapi import Header, HTTPException, Request
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.services.user import UserService


async def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


async def get_task_service(request: Request) -> UserService:
    return request.app.state.task_service


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def verify_auth_token(authorization: str = Header(..., alias="Authorization")) -> None:
    if authorization != settings.AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API token"
        )
