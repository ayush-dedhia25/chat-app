from flask_socketio import emit, join_room, leave_room

from .extensions import socketio


@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("message", {"msg": f"{data['username']} has joined the room."}, room=room)


@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    leave_room(room)
    emit("message", {"msg": f"{data['username']} has left the room."}, room=room)


@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    emit("message", {"msg": data["msg"], "username": data["username"]}, room=room)
