from enum import Enum


class ApplicationErrors(Enum):
    AUTH_TOKEN_MISSING = "AUTH_TOKEN_MISSING"
    AUTH_TOKEN_INVALID_FORMAT = "AUTH_TOKEN_INVALID_FORMAT"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
    AUTH_TOKEN_DECODE_ERROR = "AUTH_TOKEN_DECODE_ERROR"
    AUTH_USER_NOT_FOUND = "AUTH_USER_NOT_FOUND"
    AUTH_DATABASE_ERROR = "AUTH_DATABASE_ERROR"


class AppException(Exception):
    def __init__(
        self, error_code: ApplicationErrors, error: str, message: str, status_code: int
    ):
        """
        Base class for AppException instance.

        :param error_code: the error code for the exception
        :param error: the error message
        :param message: a custom message to be returned in the response
        :param status_code: the status code to be returned in the response
        """
        self.error_code = error_code
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
