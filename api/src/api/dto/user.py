from enums import UserRole
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int
    username: str
    role: UserRole = UserRole.USER


class AuthUserRequest(BaseModel):
    id: int
    username: str


class SignUpUserRequest(BaseModel):
    id: int = Field(..., description="Уникальный Telegram user_id")
    username: str | None = Field(None, description="Telegram username")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str | None = Field(None, description="Фамилия пользователя")
    language_code: str | None = Field(None, description="Код языка, например 'ru', 'en'")
