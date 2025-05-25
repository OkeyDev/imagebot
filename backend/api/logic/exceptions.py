class NotPossibleToCreateUser(Exception):
    pass


class TryAgainError(NotPossibleToCreateUser):
    def __str__(self) -> str:
        return "Try create user again"


class EmailAlreadyUsed(NotPossibleToCreateUser):
    def __init__(self, email: str) -> None:
        self.email = email

    def __str__(self) -> str:
        return f'User with email "{self.email}" already exists'


class UsernameAlreadyUsed(NotPossibleToCreateUser):
    def __init__(self, username) -> None:
        self.username = username

    def __str__(self) -> str:
        return f'Username "{self.username}" already in use. Try another'


class InvalidTokenError(Exception):
    def __init__(self, token: str) -> None:
        self.token = token

    def __str__(self) -> str:
        return f"Token {self.token} is invalid"
