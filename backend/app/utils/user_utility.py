from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models import Chat, ChatMember, ChatRequest, User


def create_user(fullName: str, username: str, email: str, password: str):
    """
    Create a new user in the database.

    Args:
        username (str): The desired username
        email (str): The email address of the user
        password (str): The desired password

    Returns:
        tuple: (user, message, status_code)
            user: The newly created user, or None if an error occurred
            message: A message indicating the outcome of the operation
            status_code: An HTTP status code indicating the outcome of the operation
    """
    if User.query.filter_by(email=email).first():
        return None, "User with this email already exists", 409

    if User.query.filter_by(username=username).first():
        return None, "Username already taken, please choose a different username", 409

    hashed_password = generate_password_hash(password)
    new_user = User(
        name=fullName,
        username=username,
        email=email,
        password_hash=hashed_password,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user, "User registered successfully", 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return None, f"An error occurred: {str(e)}", 500


def get_user_by_id(user_id: str):
    """
    Get a user by their ID.

    Args:
        user_id: The ID to search for

    Returns:
        The matching user, or None if no user is found
    """
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email: str):
    """
    Get a user by their email.

    Args:
        email: The email to search for

    Returns:
        The matching user, or None if no user is found
    """
    return User.query.filter_by(email=email).first()


def update_user(user_id: str, **kwargs):
    """
    Update a user.

    Args:
        user_id: The ID of the user to update
        **kwargs: The fields to update and their new values

    Returns:
        tuple: (user, message, status_code)
            user: The updated user
            message: A message indicating the outcome of the operation
            status_code: An HTTP status code indicating the outcome of the operation
    """
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found", 404

    try:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()
        return user, "User updated successfully", 200
    except Exception as e:
        db.session.rollback()
        return None, f"An error occurred: {str(e)}", 500


def delete_user(user_id: str):
    """
    Delete a user.

    :param user_id: The ID of the user to delete
    :return: Boolean indicating success, a message string
    """
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found"

    try:
        db.session.delete(user)
        db.session.commit()
        return True, "User deleted successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"


def change_password(user_id: str, new_password: str):
    """
    Change the password of a user.

    :param user_id: The ID of the user whose password to change
    :param new_password: The new password to set
    :return: Boolean indicating success, a message string
    """
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found"

    try:
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return True, "Password changed successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"


def get_relationship_status(user_id: str, other_user_id: str):
    # Check if there is an existing chat (i.e. they are already friends)
    existing_chat = (
        Chat.query.filter(Chat.chat_type == "one-on-one")
        .join(ChatMember)
        .filter(ChatMember.member_id.in_([user_id, other_user_id]))
        .group_by(Chat.id)
        .having(db.func.count(Chat.id) == 2)
        .first()
    )

    if existing_chat:
        return "friends"

    # Check if pending chat request exists
    existing_request = ChatRequest.query.filter_by(
        sender_id=user_id, receiver_id=other_user_id, status="pending"
    ).first()

    if existing_request:
        return "requested"

    return "unknown"
