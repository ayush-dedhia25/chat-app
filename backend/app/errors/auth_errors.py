from . import AppException, ApplicationErrors


class UserNotFound(AppException):
    def __init__(self):
        """
        Initializes an instance of the AuthUserNotFound class.

        :return: an instance of AuthUserNotFound
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_USER_NOT_FOUND,
            error="User not found",
            message="The user associated with the authentication token no longer exists.",
            status_code=404,
        )
