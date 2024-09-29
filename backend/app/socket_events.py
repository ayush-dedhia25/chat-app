from flask import request, session
from flask_socketio import disconnect, emit, join_room, leave_room
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db, socketio
from .models import ChatMember, Message, User
from .utils.jwt_utility import get_user_id_from_token

connect_users = {}


@socketio.on("connect")
def handle_connect(auth):
    token = auth.get("token") if auth else None

    if not token and "Authorization" in request.headers:
        token = request.headers.get("Authorization")

    if not token:
        print("No token provided")
        return False  # Reject the connection

    user_id = get_user_id_from_token(token)
    if not user_id:
        print("No user id found in token")
        return False  # Reject the connection

    user = User.query.get(user_id)
    if not user:
        print("User not found")
        disconnect()
        return False  # Reject the connection

    # Store user's information in the session
    session["user_id"] = user_id
    session["user"] = {"id": user.id, "name": user.name, "username": user.username}

    # Add user to the list of connected users
    connect_users[user_id] = request.sid

    # User joins their own room for personal notifications
    join_room(f"user_{user_id}")

    print(f"User {user_id} connected to the socket")
    print(f"🟢 :: Client connected to the socket")


@socketio.on("join-chat")
def handle_join_chat(data):
    user_id = session.get("user_id")
    if not user_id:
        disconnect()
        return False

    chat_id = data.get("chat_id")
    if not chat_id:
        emit("error", {"message": "Chat ID is required to join a chat"})
        return False

    # Check if user is a member of the chat
    is_member = ChatMember.query.filter_by(chat_id=chat_id, member_id=user_id).first()
    if not is_member:
        emit("error", {"message": "You are not a member of this chat"})
        return False

    join_room(f"chat_{chat_id}")
    emit("joined-chat", {"chat_id": chat_id})


@socketio.on("send-message")
def handle_send_message(data):
    user_id = session.get("user_id")
    if not user_id:
        disconnect()
        return False

    chat_id = data.get("chat_id")
    content = data.get("content")

    if not chat_id or not content:
        emit(
            "send-message:error",
            {"message": "Chat ID and content are required to send a message"},
        )
        return False

    # Check if user is a member of the chat
    is_member = ChatMember.query.filter_by(chat_id=chat_id, member_id=user_id).first()
    if not is_member:
        emit("send-message:error", {"message": "You are not a member of this chat"})
        return False

    # Create a new message
    message = Message(content=content, sender_id=user_id, chat_id=chat_id)

    try:
        db.session.add(message)
        db.session.commit()

        # Prepare message data
        message_data = {
            "id": message.id,
            "content": message.content,
            "sent_at": message.sent_at.isoformat(),
            "chat_id": chat_id,
            "sender_id": user_id,
        }

        emit("new-message", message_data, room=f"chat_{chat_id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        emit("send-message:error", {"message": str(e)})
        return False


@socketio.on("leave_chat")
def handle_leave_chat(data):
    user_id = session.get("user_id")
    if not user_id:
        disconnect()
        return False

    chat_id = data.get("chat_id")
    if not chat_id:
        emit("error", {"message": "Chat ID is required to leave a chat"})
        return False

    # Leave the chat room
    leave_room(f"chat_{chat_id}")
    emit("left-chat", {"chat_id": chat_id})
    print(f"User {user_id} left chat {chat_id}")


@socketio.on("disconnect")
def handle_disconnect():
    user_id = session.get("user_id")
    if user_id in connect_users:
        # Remove user from the list of connected users
        del connect_users[user_id]
    print(f"User {user_id} disconnected from the socket")
    print(f"🔴 :: Client disconnected from the socket")
