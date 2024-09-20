import re
import uuid
from datetime import datetime, timezone
from email.policy import default

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
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(
        db.String, nullable=True
    )  # Optional for profile pictures
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship("Message", backref="author", lazy=True)
    chat_memberships = db.relationship("ChatMember", backref="member", lazy=True)
    media = db.relationship("Media", backref="uploader", lazy=True)


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String, nullable=True)  # For group chats
    type = db.Column(db.String, nullable=False)  # 'group' or 'one-on-one'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship("Message", backref="chat", lazy=True)
    chat_memberships = db.relationship("ChatMember", backref="chat", lazy=True)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    content = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    chat_id = db.Column(db.String, db.ForeignKey("chats.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    media_id = db.Column(
        db.String, db.ForeignKey("media.id"), nullable=True
    )  # For files and images


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    url = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)  # 'image', 'file'
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    uploaded_by = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)


class ChatMember(db.Model):
    __tablename__ = "chat_members"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    chat_id = db.Column(db.String, db.ForeignKey("chats.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String, nullable=False)  # 'admin', 'member'
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ChatRequest(db.Model):
    __tablename__ = "chat_requests"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    sender_id = db.Column(
        db.String, db.ForeignKey("users.id"), nullable=False, index=True
    )
    receiver_id = db.Column(
        db.String, db.ForeignKey("users.id"), nullable=False, index=True
    )
    status = db.Column(db.String, nullable=False, default="pending", index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    sender = db.relationship(
        "User", foreign_keys=[sender_id], backref="sent_chat_requests"
    )
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], backref="received_chat_requests"
    )
