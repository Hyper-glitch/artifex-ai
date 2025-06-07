import pytest
from faker import Faker

from api.dto.user import SignUpUserRequest, SignInUserRequest

fake = Faker("ru_RU")


@pytest.fixture()
def fake_user_factory():
    """Генерация данных через Faker с фиксированным username и разными email."""
    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()

    def _user(fixed_username: bool = False) -> SignUpUserRequest:
        return SignUpUserRequest(
            id=fake.unique.random_int(min=1, max=1000000),
            username=username if fixed_username else fake.user_name(),
            first_name=fake.unique.first_name() if fixed_username else first_name,
            last_name=fake.unique.last_name() if fixed_username else last_name,
        )

    return _user


@pytest.fixture()
def user(fake_user_factory) -> SignUpUserRequest:
    return fake_user_factory()


@pytest.fixture()
def user_already_exists(fake_user_factory) -> tuple:
    first_user = fake_user_factory(fixed_username=True).model_dump()
    second_user = fake_user_factory(fixed_username=True).model_dump()

    return first_user, second_user


@pytest.fixture()
def user_data(fake_user_factory):
    return fake_user_factory()


@pytest.fixture()
def sign_in_user_not_found(user: SignUpUserRequest) -> SignInUserRequest:
    return SignInUserRequest(id=user.id, username=user.username)
