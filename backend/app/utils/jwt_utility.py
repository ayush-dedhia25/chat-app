from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from flask import current_app


def create_access_token(data: Any, expires_delta: timedelta = None):
    """
    Create a JWT access token containing the user_id.

    Args:
        data (dict): A dictionary containing the user_id to be stored in the token
        expires_delta (timedelta, optional): The time in seconds that the token should expire
            in. Defaults to 1 hour.

    Returns:
        str: The encoded JWT token
    """
    jwt_secret = current_app.config["SECRET_KEY"]

    if expires_delta is None:
        expires_delta = timedelta(hours=1)

    expire = datetime.now(timezone.utc) + expires_delta

    return jwt.encode(
        {
            "user_id": data["user_id"],
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        },
        jwt_secret,
        algorithm="HS256",
    )


def decode_access_token(token: str):
    """
    Decode a JWT access token and return the payload.

    Args:
        token (str): The JWT access token to decode

    Returns:
        dict: The decoded payload, or None if the token is invalid or expired
    """
    try:
        jwt_secret = current_app.config["SECRET_KEY"]
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_id_from_token(token: str):
    """
    Get the user_id from a JWT access token.

    Args:
        token (str): The JWT access token

    Returns:
        str: The user_id if the token is valid, None otherwise
    """
    payload = decode_access_token(token)
    if payload:
        return payload.get("user_id")
    return None


def is_token_valid(token: str):
    """
    Check if a JWT access token is valid.

    Args:
        token (str): The JWT access token to check

    Returns:
        bool: True if the token is valid, False otherwise
    """
    return decode_access_token(token) is not None


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT refresh token containing the user_id.

    Args:
        data (dict): A dictionary containing the user_id to be stored in the token
        expires_delta (timedelta, optional): The time in seconds that the token should expire
            in. Defaults to 7 days.

    Returns:
        str: The encoded JWT refresh token
    """
    if expires_delta is None:
        expires_delta = timedelta(days=7)

    return create_access_token(data, expires_delta)


def refresh_access_token(token: str):
    """
    Refresh an access token.

    Args:
        token (str): The JWT refresh token

    Returns:
        str: The new access token if the token is valid, None otherwise
    """
    user_id = get_user_id_from_token(token)
    if user_id:
        return create_access_token({"user_id": user_id})
    return None
