from datetime import datetime, timezone

from flask import Blueprint, request
from sqlalchemy import and_, desc, func
from sqlalchemy.orm import joinedload

from ..extensions import db, socketio
from ..models import Chat, ChatMember, ChatRequest, Message, User
from ..utils.protected_route import access_required
from ..utils.response import send_response

chats = Blueprint("chats", __name__, url_prefix="/chats")


@chats.route("/", methods=["GET"], strict_slashes=False)
@access_required
def get_conversations(user):
    # Subquery to get the latest message for each chat
    last_message_subq = (
        db.session.query(
            Message.chat_id, func.max(Message.sent_at).label("last_sent_at")
        )
        .group_by(Message.chat_id)
        .subquery()
    )

    # Join the subquery with the message table to get the last message details
    last_message = (
        db.session.query(
            Message.id,
            Message.chat_id,
            Message.content,
            Message.sent_at,
            Message.sender_id,
            User.username.label("sender_username"),
            last_message_subq.c.last_sent_at.label("last_message_sent_at"),
        )
        .join(
            last_message_subq,
            and_(
                Message.chat_id == last_message_subq.c.chat_id,
                Message.sent_at == last_message_subq.c.last_sent_at,
            ),
        )
        .join(User, Message.sender_id == User.id)
        .subquery()
    )

    # Retrieve chats where the user is a member
    user_chats = (
        Chat.query.join(ChatMember)
        .filter(ChatMember.member_id == user.id)
        .options(joinedload(Chat.memberships).joinedload(ChatMember.member))
        .outerjoin(last_message, last_message.c.chat_id == Chat.id)
        .add_columns(
            last_message.c.id.label("last_message_id"),
            last_message.c.content.label("last_message_content"),
            last_message.c.sent_at.label("last_message_sent_at"),
            last_message.c.sender_id.label("last_message_sender_id"),
            last_message.c.sender_username.label("last_message_sender_username"),
        )
        .order_by(desc(last_message.c.last_message_sent_at))
        .all()
    )

    chats_data = []
    for chat_tuple in user_chats:
        chat = chat_tuple[0]
        last_message_id = chat_tuple[1]
        last_message_content = chat_tuple[2]
        last_message_sent_at = chat_tuple[3]
        last_message_sender_id = chat_tuple[4]
        last_message_sender_username = chat_tuple[5]

        # Determine the members data based on chat type
        if chat.chat_type == "one-on-one":
            # Get the friend (other member) data
            friend_member = next(
                (member for member in chat.memberships if member.member.id != user.id),
                None,
            )
            if friend_member:
                members_data = {
                    "id": friend_member.member.id,
                    "name": friend_member.member.name,
                    "username": friend_member.member.username,
                    "profile_picture": friend_member.member.profile_picture,
                    "email": friend_member.member.email,
                }
            else:
                # Handle the case where the friend is not found
                members_data = None
        else:
            # For group chats, include all members except the current user
            members_data = [
                {
                    "id": member.member.id,
                    "name": member.member.name,
                    "username": member.member.username,
                    "profile_picture": member.member.profile_picture,
                    "email": member.member.email,
                }
                for member in chat.memberships
                if member.member.id != user.id
            ]

        # Also include the last message if it exists
        if last_message_id:
            last_message_data = {
                "id": last_message_id,
                "content": last_message_content,
                "sent_at": last_message_sent_at.isoformat(),
                "sender": {
                    "id": last_message_sender_id,
                    "name": last_message_sender_username,
                },
            }
        else:
            last_message_data = None  # No messages in the chat yet

        chat_info = {
            "id": chat.id,
            "name": chat.name,
            "chat_type": chat.chat_type,
            "created_at": chat.created_at.isoformat(),
            "updated_at": chat.updated_at.isoformat(),
            "members": members_data,
            "last_message": last_message_data,
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
        "chat_id": chat_request.id,
        "sender": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "profile_picture": user.profile_picture,
        },
        "created_at": chat_request.created_at.isoformat(),
    }

    socketio.emit(
        "incoming-chat-request",
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
            "chat-request:accepted",
            response_data,
            to=f"user_{chat_request.sender_id}",
        )
    else:
        chat_request.status = status
        db.session.commit()

        # Notify the sender about the request rejection
        response_data = {"request_id": request_id, "status": "rejected"}
        socketio.emit(
            "chat-request:rejected",
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
            "sender": {
                "id": request.sender_id,
                "name": sender.name if sender else None,
                "username": sender.username if sender else None,
                "profile_picture": sender.profile_picture if sender else None,
            },
            "created_at": request.created_at.isoformat(),
        }
        requests_data.append(request_info)

    return send_response(
        data=requests_data,
        message="Chat requests fetched successfully",
        success=True,
        status_code=200,
    )


@chats.route("/<string:chat_id>/messages", methods=["GET"])
@access_required
def get_chat_messages(user, chat_id):
    is_member = ChatMember.query.filter_by(chat_id=chat_id, member_id=user.id).first()
    if not is_member:
        return send_response(
            message="You are not a member of this chat.", success=False, status_code=403
        )

    # Fetch the chat with its members
    chat = (
        Chat.query.filter_by(id=chat_id)
        .options(joinedload(Chat.memberships).joinedload(ChatMember.member))
        .first()
    )
    if not chat:
        return send_response(message="Chat not found.", success=False, status_code=404)

    # Determine the friend's data for one-on-one chats
    if chat.chat_type == "one-on-one":
        friend_member = next(
            (member for member in chat.memberships if member.member_id != user.id), None
        )
        if friend_member:
            friend = friend_member.member
            friend_data = {
                "id": friend.id,
                "name": friend.name,
                "username": friend.username,
                "profile_picture": friend.profile_picture,
                "email": friend.email,
            }
        else:
            return send_response(
                message="Friend not found in the chat.", success=False, status_code=404
            )
    else:
        # For group chats, fetch the friend's data
        friend_data = None

    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = (
        Message.query.filter_by(chat_id=chat_id)
        .options(joinedload(Message.author))
        .order_by(Message.sent_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    messages = pagination.items

    # Build messages data
    messages_data = [
        {
            "id": message.id,
            "content": message.content,
            "sent_at": message.sent_at.isoformat(),
            "sender": {
                "id": message.sender_id,
                "name": message.author.name,
                "username": message.author.username,
                "profile_picture": message.author.profile_picture,
            },
        }
        for message in messages
    ]

    pagination_info = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
    }

    response_data = {
        "friend": friend_data,
        "messages": messages_data,
        "pagination": pagination_info,
    }

    return send_response(
        data=response_data,
        message="Messages fetched successfully",
        success=True,
        status_code=200,
    )
