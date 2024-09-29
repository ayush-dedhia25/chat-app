import uuid
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint

from .extensions import db


def generate_uuid():
    """
    Generates a random UUID and returns it as a string.

    Returns:
        str: A random UUID
    """
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String, nullable=False, index=True)
    username = db.Column(db.String, unique=True, nullable=False, index=True)
    email = db.Column(db.String, unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(
        db.String, nullable=True
    )  # Optional for profile pictures
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship("Message", back_populates="author", lazy="dynamic")
    chat_memberships = db.relationship(
        "ChatMember", back_populates="member", lazy="dynamic"
    )
    media = db.relationship("Media", back_populates="uploader", lazy="dynamic")
    sent_chat_requests = db.relationship(
        "ChatRequest",
        foreign_keys="ChatRequest.sender_id",
        back_populates="sender",
        lazy="dynamic",
    )
    received_chat_requests = db.relationship(
        "ChatRequest",
        foreign_keys="ChatRequest.receiver_id",
        back_populates="receiver",
        lazy="dynamic",
    )


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String, nullable=True)  # For group chats
    chat_type = db.Column(db.String, nullable=False)  # 'group' or 'one-on-one'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    messages = db.relationship("Message", back_populates="chat", lazy="dynamic")
    memberships = db.relationship(
        "ChatMember",
        back_populates="chat",
        lazy="select",
        cascade="all, delete-orphan",
    )


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    content = db.Column(db.Text, nullable=True)
    sent_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    chat_id = db.Column(
        db.String, db.ForeignKey("chats.id"), nullable=False, index=True
    )
    sender_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    media_id = db.Column(
        db.String, db.ForeignKey("media.id"), nullable=True
    )  # For files and images

    chat = db.relationship("Chat", back_populates="messages")
    author = db.relationship("User", back_populates="messages")
    media = db.relationship("Media", back_populates="messages")

    __table_args__ = (
        CheckConstraint(
            "(content IS NOT NULL) OR (media_id IS NOT NULL)",
            name="check_content_or_media_id",
        ),
    )


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    url = db.Column(db.String, nullable=False)
    media_type = db.Column(db.String, nullable=False)  # 'image', 'file'
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    uploader_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)

    uploader = db.relationship("User", back_populates="media")
    messages = db.relationship("Message", back_populates="media")


class ChatMember(db.Model):
    __tablename__ = "chat_members"

    chat_id = db.Column(db.String, db.ForeignKey("chats.id"), primary_key=True)
    member_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    member_role = db.Column(db.String, nullable=False)  # 'admin', 'member'
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    chat = db.relationship("Chat", back_populates="memberships")
    member = db.relationship("User", back_populates="chat_memberships")


class ChatRequest(db.Model):
    __tablename__ = "chat_requests"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    sender_id = db.Column(
        db.String, db.ForeignKey("users.id"), nullable=False, index=True
    )
    receiver_id = db.Column(
        db.String, db.ForeignKey("users.id"), nullable=False, index=True
    )
    status = db.Column(
        db.String, nullable=False, default="pending", index=True
    )  # 'pending', 'accepted', 'rejected'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_chat_requests",
    )
    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_chat_requests",
    )

    __table_args__ = (
        UniqueConstraint(
            "sender_id",
            "receiver_id",
            name="uq_chat_request_sender_receiver",
        ),
    )
