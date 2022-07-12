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
