from flask import Blueprint

from ..models import Chat
from ..utils.protected_route import access_required

chats = Blueprint("chats", __name__)


@chats.route("/chats")
@access_required
def get_chats(user):
    print(user)
    return {"message": "Hello, World!"}
