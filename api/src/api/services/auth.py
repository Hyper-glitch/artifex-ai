import logging
from typing import Callable

from exceptions import UserAlreadyExistsException, UserNotFoundException
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from api.dto.user import AuthUserRequest, RegisterUserRequest
from api.repositories.user import UserRepository


class AuthService:
    def __init__(self, repo_factory: Callable[[AsyncSession], UserRepository]) -> None:
        self._repo_factory = repo_factory

    async def register_user(self, user_data: RegisterUserRequest, session: AsyncSession) -> User:
        """Регистрирует нового пользователя."""
        repo = self._repo_factory(session)
        existing_user = await repo.get_user(user_data.id, user_data.username)
        if existing_user and user_data.username == existing_user.username:
            raise UserAlreadyExistsException()

        user = await repo.create_user(user_data)
        logging.info(f"User - {user.id} - successfully registered.")

        return user

    async def auth_user(self, user_data: AuthUserRequest, session: AsyncSession) -> None:
        """Проверяет пользователя в базе данных."""
        repo = self._repo_factory(session)
        user = await repo.get_user(id=user_data.id, username=user_data.username)
        if not user:
            raise UserNotFoundException()

        logging.info(f"User - {user.id} - successfully checked in the system.")
