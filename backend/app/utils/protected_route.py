from functools import wraps

import jwt
from flask import current_app, request

from ..errors.auth_errors import UserNotFound
from ..errors.database_errors import DatabaseError
from ..errors.jwt_errors import (
    AuthTokenDecodeError,
    AuthTokenExpired,
    AuthTokenInvalid,
    AuthTokenInvalidFormat,
    AuthTokenMissing,
)
from ..models import User


def access_required(f):
    """Decorator to check if the request has a valid JWT access token.

    The JWT token should be sent in the Authorization header of the request.
    If the token is valid, the user object is passed to the decorated function.
    If the token is invalid or missing, a JSON response with a 401 status code is returned.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """Decorator to check if the request has a valid JWT access token.

        The JWT token should be sent in the Authorization header of the request.
        If the token is valid, the user object is passed to the decorated function.
        If the token is invalid or missing, a JSON response with a 401 status code is returned.
        """
        token = request.headers.get("Authorization")

        # Check if the token is present
        if not token:
            raise AuthTokenMissing()

        # Check if the token starts with "Bearer "
        if not token.startswith("Bearer "):
            raise AuthTokenInvalidFormat()

        # Split the token to get the actual token
        token = token.split(" ")[1]

        # Check if the token is valid and belongs to a user
        try:
            jwt_secret = current_app.config["SECRET_KEY"]
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthTokenExpired()
        except jwt.InvalidTokenError:
            raise AuthTokenInvalid()
        except Exception as e:
            raise AuthTokenDecodeError(str(e))

        try:
            current_user = User.query.get(data["user_id"])
            if not current_user:
                raise UserNotFound()
        except Exception as e:
            raise DatabaseError(str(e))

        return f(current_user, *args, **kwargs)

    return decorated
