from . import AppException, ApplicationErrors


class DatabaseError(AppException):
    def __init__(self, original_error: str):
        """
        Initializes an instance of the AuthDatabaseError class.

        :param original_error: the error that occurred while retrieving the user
        :return: an instance of AuthDatabaseError
        """
        super().__init__(
            error_code=ApplicationErrors.AUTH_DATABASE_ERROR,
            error="Database error",
            message=f"An error occurred while retrieving user: {original_error}",
            status_code=500,
        )
