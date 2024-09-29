from datetime import timedelta

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from ..models import User
from ..schema import login_schema, signup_schema
from ..utils.jwt_utility import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
)
from ..utils.response import send_response
from ..utils.user_utility import create_user

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    """
    Handle login requests.

    Returns a JSON response with a token to be used for protected routes
    if the credentials are valid, or a 400 status code with a JSON response
    containing validation errors if the request body is invalid.

    If the credentials are invalid, returns a 404 status code with a JSON
    response containing an error message.

    The token will expire in 30 minutes.
    """
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        return jsonify({"error": err.messages}), 400

    username_or_email = data.get("usernameOrEmail")
    password = data.get("password")

    if "@" in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(name=username_or_email).first()

    if not user:
        return send_response(
            message="User with that email or username not found",
            success=False,
            status_code=404,
        )

    if user and check_password_hash(user.password_hash, password):
        token_payload = {"user_id": user.id}

        # Generate access and refresh tokens
        token_expiration_time = timedelta(minutes=30)
        token = create_access_token(token_payload, expires_delta=token_expiration_time)
        refresh_token = create_refresh_token(
            token_payload, expires_delta=timedelta(days=7)
        )

        # Respond with the tokens and user info
        return send_response(
            data={
                "token": token,
                "refreshToken": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_picture": user.profile_picture,
                },
            },
            message="Login successful",
            status_code=200,
            success=True,
        )

    return send_response(status_code=404, success=False, message="Invalid credentials")


@auth.route("/sign-up", methods=["POST"])
def signup():
    """
    Create a new user and return a JSON response with a message and
    the corresponding HTTP status code.

    The request body should contain the username, email, and password in
    JSON format.

    Returns:
        A JSON response with a message and the corresponding HTTP status code
    """
    try:
        data = signup_schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        return send_response(
            data={"error": err.messages},
            status_code=400,
            success=False,
        )

    user, message, status_code = create_user(
        data["fullName"], data["username"], data["email"], data["password"]
    )

    return send_response(
        message=message, status_code=status_code, success=user is not None
    )


@auth.route("/refresh", methods=["POST"])
def refresh_token():
    """
    Refresh an access token using a refresh token.

    The request body should contain the refresh token in JSON format.

    Returns:
        A JSON response with the new access token and the corresponding HTTP status code
    """
    try:
        body = request.json
        refresh_token = body.get("refreshToken")

        if not refresh_token:
            return send_response(
                success=False, message="Refresh token is required", status_code=400
            )

        # Refresh the access token using the refresh token
        new_access_token = refresh_access_token(refresh_token)

        if not new_access_token:
            return send_response(
                success=False,
                message="Invalid or expired refresh token",
                status_code=401,
            )

        # Return the new access token
        return send_response(
            data={"token": new_access_token}, success=True, status_code=200
        )
    except Exception as e:
        print(f"Error refreshing token: {str(e)}")
        return send_response(
            success=False, message="Failed to refresh token", status_code=500
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
