from datetime import datetime, timezone

from .extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
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

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=True)  # For group chats
    type = db.Column(db.String, nullable=False)  # 'group' or 'one-on-one'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship("Message", backref="chat", lazy=True)
    chat_memberships = db.relationship("ChatMember", backref="chat", lazy=True)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.String, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    chat_id = db.Column(db.String, db.ForeignKey("chats.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    media_id = db.Column(
        db.String, db.ForeignKey("media.id"), nullable=True
    )  # For files and images


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)  # 'image', 'file'
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    uploaded_by = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)


class ChatMember(db.Model):
    __tablename__ = "chat_members"

    id = db.Column(db.String, primary_key=True)
    chat_id = db.Column(db.String, db.ForeignKey("chats.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String, nullable=False)  # 'admin', 'member'
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
