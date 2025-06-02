from enum import StrEnum

from starlette import status


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class TaskStatus(StrEnum):
    NEW = "new"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SignUpStatus(StrEnum):
    CREATED = "created"
    ALREADY_EXISTS = "already_exists"

    @property
    def http_status(self) -> int:
        return {
            self.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
            self.CREATED: status.HTTP_201_CREATED,
        }.get(self, status.HTTP_500_INTERNAL_SERVER_ERROR)
