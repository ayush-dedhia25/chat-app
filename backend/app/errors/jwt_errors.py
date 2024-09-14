from . import AppException, ApplicationErrors


class AuthTokenMissing(AppException):
    def __init__(self):
        """
        Initializes an instance of the AuthTokenMissing class.

        :return: an instance of AuthTokenMissing
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_TOKEN_MISSING,
            error="Authentication denied",
            message="Authentication token is missing.",
            status_code=401,
        )


class AuthTokenInvalidFormat(AppException):
    def __init__(self):
        """
        Initializes an instance of the AuthTokenInvalidFormat class.

        :return: an instance of AuthTokenInvalidFormat
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_TOKEN_INVALID_FORMAT,
            error="Invalid token format",
            message="Authentication token must start with 'Bearer '",
            status_code=401,
        )


class AuthTokenExpired(AppException):
    def __init__(self):
        """
        Initializes an instance of the AuthTokenExpired class.

        :return: an instance of AuthTokenExpired
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_TOKEN_EXPIRED,
            error="Authentication token expired",
            message="Authentication token has expired. Please login again.",
            status_code=401,
        )


class AuthTokenInvalid(AppException):
    def __init__(self):
        """
        Initializes an instance of the AuthTokenInvalid class.

        :return: an instance of AuthTokenInvalid
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_TOKEN_INVALID,
            error="Invalid authentication token",
            message="The authentication token is invalid.",
            status_code=401,
        )


class AuthTokenDecodeError(AppException):
    def __init__(self, original_error: str):
        """
        Initializes an instance of the AuthTokenDecodeError class.

        :param original_error: the error that occurred while decoding the authentication token
        :return: an instance of AuthTokenDecodeError
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_TOKEN_DECODE_ERROR,
            error="Failed to decode authentication token",
            message=f"An error occurred while decoding the authentication token: {original_error}",
            status_code=401,
        )
