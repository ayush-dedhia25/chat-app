from flask import Blueprint


chats = Blueprint("chats", __name__)


@chats.route("/chats")
def get_chats():
    return {"message": "Hello, World!"}
