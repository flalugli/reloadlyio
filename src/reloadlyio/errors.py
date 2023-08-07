
class ReloadlyError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidCredentials(ReloadlyError):
    def __init__(self, message: str = "The credentials passed are invalid") -> None:
        super().__init__(message)

