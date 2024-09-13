from functools import wraps
from flask import current_app, jsonify, request
import jwt

from ..models import User


def access_required(f):
    """Decorator to check if the request has a valid JWT access token.

    The JWT token should be sent in the Authorization header of the request.
    If the token is valid, the user object is passed to the decorated function.
    If the token is invalid or missing, a JSON response with a 401 status code is returned.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Decorated function to check if the request has a valid JWT access token.

        The JWT token should be sent in the Authorization header of the request.
        If the token is valid, the user object is passed to the decorated function.
        If the token is invalid or missing, a JSON response with a 401 status code is returned.
        """
        token = request.headers.get("Authorization")

        # Check if the token is present
        if not token:
            return {"message": "Authentication denied, no auth token provided"}, 401

        # Check if the token starts with "Bearer "
        if not token.startswith("Bearer "):
            return {"message": "Invalid token format"}, 401

        # Split the token to get the actual token
        token = token.split(" ")[1]

        # Check if the token is valid and belongs to a user
        try:
            jwt_secret = current_app.config["SECRET_KEY"]
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["user_id"]).first()
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)

    return decorated
