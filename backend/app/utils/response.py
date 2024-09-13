from typing import Any
from flask import jsonify


def send_response(
    data: Any = None, message: str = None, success: bool = True, status_code: int = 200
):
    """
    Helper function to return a JSON response with a given status code.

    :param data: The data to be returned in the response
    :param message: A custom message to be returned in the response. If not
        provided, a default message indicating success or failure is used.
    :param success: A boolean indicating whether the request was successful
    :param status_code: The HTTP status code to return

    :return: A tuple containing the JSON response and the status code
    """
    response = {
        "success": success,
        "message": (
            message
            if message
            else ("Request was successful" if success else "Request failed")
        ),
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code
