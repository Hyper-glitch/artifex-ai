import logging
from typing import Callable

from api.exceptions import UserNotFoundException
from enums import SignUpStatus
from sqlalchemy.ext.asyncio import AsyncSession

from api.dto.user import SignInUserRequest, SignUpUserRequest
from api.repositories.user import UserRepository


class UserService:
    def __init__(self, repo_factory: Callable[[AsyncSession], UserRepository]) -> None:
        self._repo_factory = repo_factory

    async def sign_up(self, user_data: SignUpUserRequest, session: AsyncSession) -> SignUpStatus:
        """Регистрирует нового пользователя."""
        repo = self._repo_factory(session)
        existing_user = await repo.get_user(user_data.id, user_data.username)
        if existing_user:
            return SignUpStatus.ALREADY_EXISTS

        await repo.create_user(user_data)
        logging.info(f"User - {user_data.id} - successfully registered.")
        return SignUpStatus.CREATED

    async def auth(self, user_data: SignInUserRequest, session: AsyncSession) -> None:
        """Проверяет пользователя в базе данных."""
        repo = self._repo_factory(session)
        user = await repo.get_user(id=user_data.id, username=user_data.username)
        if not user:
            raise UserNotFoundException()

        logging.info(f"User - {user.id} - successfully checked in the system.")
