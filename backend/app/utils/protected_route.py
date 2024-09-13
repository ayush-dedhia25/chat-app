from functools import wraps
from flask import current_app, jsonify, request
import jwt

from ..models import User


def access_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401
        try:
            jwt_secret = current_app.config["SECRET_KEY"]
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["user_id"]).first()
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)

    return decorated
