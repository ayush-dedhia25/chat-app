from flask import Blueprint

from ..utils.protected_route import access_required

from ..models import Chat


chats = Blueprint("chats", __name__)


@chats.route("/chats")
@access_required
def get_chats(user):
    print(user)
    return {"message": "Hello, World!"}
