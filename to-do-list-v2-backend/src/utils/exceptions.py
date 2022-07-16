from fastapi import HTTPException, status


class APIException(HTTPException):
    status_code: int
    detail: str
    description: str

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class InvalidTokenError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token"
    description = "This access token is invalid."


class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"
    description = "The user is not allowed to use this endpoint."


class InvalidCredentials(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid username or password"
    description = "The username or password ar not registered."


class AccountDisabled(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Account is disabled"
    description = "This account was disabled by an admin."


class NameDuplicated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Name is already in use"
    description = "This name is already taken by another user."


class InvalidTask(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Task not found"
    description = "This task does not exist."


