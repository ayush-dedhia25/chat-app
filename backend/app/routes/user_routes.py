from flask import Blueprint, request
from sqlalchemy import case, or_
from sqlalchemy.orm import aliased

from ..extensions import db
from ..models import Chat, ChatMember, ChatRequest, User
from ..utils.protected_route import access_required
from ..utils.response import send_response

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"], strict_slashes=False)
@access_required
def search_users(current_user):
    search_query = request.args.get("query", "").strip()
    if not search_query:
        return send_response(
            data=[], message="No search query provided", success=True, status_code=200
        )

    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Aliases for tables
    ChatMember1 = aliased(ChatMember)
    ChatMember2 = aliased(ChatMember)
    # IncomingRequest = aliased(ChatRequest)
    # OutgoingRequest = aliased(ChatRequest)

    # Subquery to check for the existing chats
    existing_chats_subq = (
        db.session.query(Chat.id)
        .join(ChatMember1, ChatMember1.chat_id == Chat.id)
        .join(ChatMember2, ChatMember2.chat_id == Chat.id)
        .filter(
            Chat.chat_type == "one-on-one",
            ChatMember1.member_id == current_user.id,
            ChatMember2.member_id == User.id,
            ChatMember1.member_id != ChatMember2.member_id,
        )
        .exists()
    )

    existing_requests_subq = (
        db.session.query(ChatRequest.id)
        .filter(
            ChatRequest.sender_id == current_user.id,
            ChatRequest.receiver_id == User.id,
            ChatRequest.status == "pending",
        )
        .exists()
    )

    # Subquery to check for incoming chat requests
    incoming_requests_subq = (
        db.session.query(ChatRequest.id)
        .filter(
            ChatRequest.sender_id == User.id,
            ChatRequest.receiver_id == current_user.id,
            ChatRequest.status == "pending",
        )
        .exists()
    )

    # Scalar subquery to get request IDs
    incoming_request_id_subq = (
        db.session.query(ChatRequest.id)
        .filter(
            ChatRequest.sender_id == User.id,
            ChatRequest.receiver_id == current_user.id,
            ChatRequest.status == "pending",
        )
        .correlate(User)
        .scalar_subquery()
    )

    outgoing_request_id_subq = (
        db.session.query(ChatRequest.id)
        .filter(
            ChatRequest.sender_id == current_user.id,
            ChatRequest.receiver_id == User.id,
            ChatRequest.status == "pending",
        )
        .correlate(User)
        .scalar_subquery()
    )

    # Build the main query
    users_query = (
        User.query.filter(User.id != current_user.id)
        .filter(
            or_(
                User.username.ilike(f"%{search_query}%"),
                User.name.ilike(f"%{search_query}%"),
            )
        )
        .add_columns(
            case(
                (existing_chats_subq, "friends"),
                else_=case(
                    (existing_requests_subq, "request_sent"),
                    else_=case(
                        (incoming_requests_subq, "request_received"), else_="unknown"
                    ),
                ),
            ).label("relationship_status"),
            incoming_request_id_subq.label("incoming_request_id"),
            outgoing_request_id_subq.label("outgoing_request_id"),
        )
    )

    # Pagination
    pagination = users_query.paginate(page=page, per_page=per_page, error_out=False)
    matching_users = pagination.items

    # Build the response data
    results = []
    for data_tuple in matching_users:
        user = data_tuple[0]
        relationship_status = data_tuple[1]
        incoming_request_id = data_tuple[2]
        outgoing_request_id = data_tuple[3]

        user_info = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture,
            "relationship_status": relationship_status,
        }

        # Include the reuest_id when the relationship_status is "request_received" or "request_sent"
        if relationship_status == "request_received":
            user_info["request_id"] = incoming_request_id
        elif relationship_status == "request_sent":
            user_info["request_id"] = outgoing_request_id

        results.append(user_info)

    pagination_info = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
    }

    return send_response(
        data={"results": results, "pagination": pagination_info},
        message="Users fetched successfully",
        success=True,
        status_code=200,
    )
