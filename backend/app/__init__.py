from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .extensions import db, socketio

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
    app.config["SECRET_KEY"] = "your_secret_key"

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)
    socketio.init_app(app)

    from .routes import chats as chats_blueprint, auth as auth_blueprint

    app.register_blueprint(chats_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
