import pytest
from fastapi import status
from httpx import AsyncClient

from api.dto.user import SignUpUserRequest, SignInUserRequest


class TestUserService:
    _sign_up_url = "/users/sign-up/"
    _sign_in_url = "/users/sign-in/"

    @pytest.mark.asyncio
    async def test_sign_up_success(self, async_client: AsyncClient, user: SignUpUserRequest) -> None:
        """Тест успешной регистрации пользователя."""
        response = await async_client.post(self._sign_up_url, json=user.model_dump())

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"success": True}

    @pytest.mark.asyncio
    async def test_sign_up_user_already_exists(self, async_client: AsyncClient, user_already_exists) -> None:
        """Тест ошибки при регистрации (пользователь уже существует)."""
        first_user, second_user = user_already_exists
        await async_client.post(self._sign_up_url, json=first_user)

        second_response = await async_client.post(self._sign_up_url, json=second_user)
        assert second_response.status_code == status.HTTP_409_CONFLICT
        assert second_response.json() == {"success": True}

    @pytest.mark.asyncio
    async def test_authorize_success(self, user: SignUpUserRequest, async_client: AsyncClient) -> None:
        """Тест успешной авторизации пользователя."""
        await async_client.post(self._sign_up_url, json=user.model_dump())

        dto = SignInUserRequest(id=user.id, username=user.username)
        response = await async_client.post(self._sign_in_url, json=dto.model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"success": True}

    @pytest.mark.asyncio
    async def test_authorize_user_not_found(self, async_client: AsyncClient, sign_in_user_not_found: SignInUserRequest) -> None:
        """Тест авторизации несуществующего пользователя."""
        response = await async_client.post(self._sign_in_url, json=sign_in_user_not_found.model_dump())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"success": False, "message": "User not found in the system!"}
