from flask import Flask

from ..errors import AppException
from ..utils.response import send_response


def error_handler(e: AppException):
    """
    Handles AppException errors by returning a JSON response with the error message,
    error code, and status code.

    :param e: The AppException instance
    :return: A JSON response with the error message, error code, and status code
    """
    return send_response(
        data={"error": e.error, "error_code": e.error_code.value},
        message=e.message,
        status_code=e.status_code,
        success=False,
    )


def register_app_error_handlers(app: Flask):
    """
    Registers the error handlers for the app.

    :param app: The Flask app to register the error handlers with
    """
    app.register_error_handler(AppException, error_handler)
