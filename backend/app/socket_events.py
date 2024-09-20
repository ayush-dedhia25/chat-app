from flask import request
from flask_socketio import join_room

from .extensions import socketio
from .utils.jwt_utility import get_user_id_from_token


@socketio.on("connect")
def handle_connect():
    token = request.args.get("token")
    if not token:
        return False  # Reject the connection

    user_id = get_user_id_from_token(token)
    if not user_id:
        return False  # Reject the connection

    join_room(f"user:{user_id}")
    print(f"User {user_id} connected and joined room user:{user_id}")
