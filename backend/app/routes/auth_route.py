from datetime import datetime, timezone, timedelta
from flask import Blueprint, jsonify, request, current_app
import jwt
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from ..utils.user_utility import create_user
from ..utils.response import send_response
from ..models import User
from ..schema import login_schema, signup_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    """
    Handle login requests.

    Returns a JSON response with a token to be used for protected routes
    if the credentials are valid, or a 400 status code with a JSON response
    containing validation errors if the request body is invalid.

    If the credentials are invalid, returns a 401 status code with a JSON
    response containing an error message.

    The token will expire in 1 hour.
    """
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        return jsonify({"error": err.messages}), 400

    user = User.query.filter_by(email=data["email"]).first()
    print(user)
    if user and check_password_hash(user.password, data["password"]):
        jwt_secret = current_app.config["SECRET_KEY"]
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            },
            jwt_secret,
            algorithm="HS256",
        )
        return send_response(
            data={
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_picture": user.profile_picture,
                },
            },
            message="Login successful",
        )
    return send_response(status_code=404, success=False, message="User not found")


@auth.route("/sign-up", methods=["POST"])
def signup():
    """
    Create a new user and return a JSON response with a message and
    the corresponding HTTP status code.

    The request body should contain the username, email and password in
    JSON format.

    Returns:
        A JSON response with a message and the corresponding HTTP status code
    """
    try:
        data = signup_schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        # return jsonify({"error": err.messages}), 400
        return send_response(
            data={"error": err.messages},
            status_code=400,
            success=False,
        )

    user, message, status_code = create_user(
        data["username"], data["email"], data["password"]
    )
    # return jsonify({"message": message}), status_code
    return send_response(
        message=message, status_code=status_code, success=user is not None
    )


@auth.errorhandler(500)
def internal_error(error):
    """
    Handles 500 errors by returning a JSON response with a message and
    the 500 status code.

    Args:
        error: The exception that caused the error

    Returns:
        A JSON response with a message and the 500 status code
    """
    return jsonify({"message": "An internal server error occurred"}), 500
