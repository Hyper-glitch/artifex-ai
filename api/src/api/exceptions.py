class UserAlreadyExistsException(Exception):
    def __init__(self) -> None:
        super().__init__("User already exists")


class UserNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("User not found in the system!")


class TaskNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("ML Task not found!")
