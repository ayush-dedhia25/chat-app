from datetime import datetime, timezone

from flask import Blueprint, request
from sqlalchemy.orm import joinedload

from ..extensions import db, socketio
from ..models import Chat, ChatMember, ChatRequest, User
from ..utils.protected_route import access_required
from ..utils.response import send_response

chats = Blueprint("chats", __name__, url_prefix="/chats")


@chats.route("/", methods=["GET"])
@access_required
def get_chats(user):
    # Retrieve chats where the user is a member
    user_chats = (
        Chat.query.join(ChatMember)
        .filter(ChatMember.member_id == user.id)
        .options(joinedload(Chat.memberships).joinedload(ChatMember.member))
        .all()
    )

    chats_data = []
    for chat in user_chats:
        # Get the members of the chat
        members_data = [
            {
                "id": member.member.id,
                "username": member.member.username,
                "email": member.member.email,
            }
            for member in chat.memberships
        ]

        chat_info = {
            "id": chat.id,
            "name": chat.name,
            "chat_type": chat.chat_type,
            "created_at": chat.created_at.isoformat(),
            "updated_at": chat.updated_at.isoformat(),
            "members": members_data,
        }
        chats_data.append(chat_info)

    return send_response(
        data=chats_data,
        message="Chats fetched successfully",
        success=True,
        status_code=200,
    )


@chats.route("/requests/send", methods=["POST"])
@access_required
def handle_send_chat_request(user):
    data = request.get_json()
    receiver_id = data.get("receiver_id")

    # Validate the receiver_id
    if not receiver_id:
        return send_response(
            data={"error": "Receiver ID is required"},
            message="Failed to send chat request",
            success=False,
            status_code=400,
        )

    if receiver_id == user.id:
        return send_response(
            data={"error": "You cannot send a chat request to yourself"},
            message="Failed to send chat request",
            success=False,
            status_code=400,
        )

    # Check if the receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        return send_response(
            data={"error": "User not found."},
            message="Failed to send chat request",
            success=False,
            status_code=404,
        )

    # Check if a chat already exists between the two users
    existing_chat = (
        Chat.query.filter(Chat.chat_type == "one-on-one")
        .join(ChatMember)
        .filter(ChatMember.member_id.in_([user.id, receiver_id]))
        .group_by(Chat.id)
        .having(db.func.count(Chat.id) == 2)
        .first()
    )
    if existing_chat:
        return send_response(
            data={"error": "Chat already exists with this user."},
            message="Failed to send chat request",
            success=False,
            status_code=400,
        )

    # Check if a pending chat request already exists
    existing_request = ChatRequest.query.filter_by(
        sender_id=user.id, receiver_id=receiver_id, status="pending"
    ).first()
    if existing_request:
        return send_response(
            data={"error": "Chat request already sent."},
            message="Failed to send chat request",
            success=False,
            status_code=400,
        )

    # Create a new chat request
    chat_request = ChatRequest(
        sender_id=user.id, receiver_id=receiver_id, status="pending"
    )
    db.session.add(chat_request)
    db.session.commit()

    # Notify the receiver via WebSocket
    notification_data = {
        "id": chat_request.id,
        "sender_id": user.id,
        "sender_username": user.username,
        "created_at": chat_request.created_at.isoformat(),
    }

    socketio.emit(
        "chat_request",
        notification_data,
        to=f"user_{receiver_id}",
    )

    return send_response(
        message="Chat request sent successfully", success=True, status_code=201
    )


@chats.route("/requests/receive/<string:request_id>", methods=["PUT"])
@access_required
def respond_to_chat_request(user, request_id):
    data = request.get_json()
    status = data.get("status")

    if status not in ["accepted", "rejected"]:
        return send_response(message="Invalid status", status_code=400, success=False)

    chat_request = ChatRequest.query.get(request_id)

    if not chat_request or chat_request.receiver_id != user.id:
        return send_response(
            message="Chat request not found", status_code=404, success=False
        )

    if chat_request.status != "pending":
        return send_response(
            message=f"Chat request already {chat_request.status}.",
            status_code=400,
            success=False,
        )

    chat_request.status = status
    db.session.commit()

    if status == "accepted":
        # Create a new chat
        chat = Chat(chat_type="one-on-one")
        db.session.add(chat)
        db.session.commit()

        # Add both users to the chat
        member1 = ChatMember(
            chat_id=chat.id,
            member_id=chat_request.sender_id,
            member_role="member",
            joined_at=datetime.now(timezone.utc),
        )
        member2 = ChatMember(
            chat_id=chat.id,
            member_id=user.id,
            member_role="member",
            joined_at=datetime.now(timezone.utc),
        )
        db.session.add_all([member1, member2])
        db.session.commit()

        response_data = {
            "request_id": request_id,
            "status": "accepted",
            "chat_id": chat.id,
            "chat_type": chat.chat_type,
            "created_at": chat.created_at.isoformat(),
        }
        socketio.emit(
            "chat_request:accepted",
            response_data,
            to=f"user_{chat_request.sender_id}",
        )
    else:
        chat_request.status = status
        db.session.commit()

        # Notify the sender about the request rejection
        response_data = {"request_id": request_id, "status": "rejected"}
        socketio.emit(
            "chat_request:rejected",
            response_data,
            to=f"user_{chat_request.sender_id}",
        )

    return send_response(
        message="Chat request responded successfully", success=True, status_code=200
    )


@chats.route("/requests", methods=["GET"])
@access_required
def get_chat_requests(user):
    # Fetch all pending chat requests received by the user
    pending_requests = ChatRequest.query.filter_by(
        receiver_id=user.id, status="pending"
    ).all()

    requests_data = []
    for request in pending_requests:
        sender = User.query.get(request.sender_id)
        request_info = {
            "id": request.id,
            "sender_id": request.sender_id,
            "sender_username": sender.username if sender else None,
            "created_at": request.created_at.isoformat(),
        }
        requests_data.append(request_info)

    return send_response(
        data=requests_data,
        message="Chat requests fetched successfully",
        success=True,
        status_code=200,
    )
