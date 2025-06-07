import pytest


@pytest.fixture()
async def user_service(async_session):
    """Создает мокнутый AuthService с тестовой сессией."""
    from api.services.user import UserService
    from api.repositories.user import UserRepository

    yield UserService(repo_factory=lambda session: UserRepository(async_session))


@pytest.fixture()
async def task_service(async_session):
    """Создает MLTaskService с тестовой сессией."""
    from api.services.task import TaskService
    from api.repositories.task import TaskRepository
    from api.rmq import AsyncRabbitMQProducer

    producer = AsyncRabbitMQProducer()
    yield TaskService(repo_factory=lambda session: TaskRepository(async_session), producer=producer)
