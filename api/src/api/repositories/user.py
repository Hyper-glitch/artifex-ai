import logging
from typing import Optional, Sequence

from api.dto.user import SignUpUserRequest
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class UserRepository:
    """Репозиторий для управления пользователями."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_user(self, user_data: SignUpUserRequest) -> User:
        """Создаёт нового пользователя."""
        user = User(
            id=user_data.id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            language_code=user_data.language_code,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        logging.info(f"User - {user.id} - successfully created.")

        return user

    async def get_user_by_id(self, user_id: int) -> User:
        """Получает пользователя по ID."""
        result = await self._session.execute(
            select(User).options(joinedload(User.balance)).filter(User.id == user_id)
        )
        return result.scalars().first()

    async def get_user(self, id: int, username: str | None = None) -> Optional[User]:
        """Получает пользователя по id или по username."""
        query = select(User).where((User.id == id) | (User.username == username))
        result = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_all_users(self) -> Sequence[User]:
        """Получает список всех пользователей."""
        result = await self._session.execute(select(User))
        return result.scalars().all()

    async def delete_user(self, user_id: int) -> None:
        """Удаляет пользователя по ID."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found!")

        await self._session.delete(user)
        await self._session.commit()
        logging.info(f"User - {user.id} - successfully deleted.")
