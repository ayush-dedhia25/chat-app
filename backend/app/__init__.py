from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    from flask import Flask
    from flask_cors import CORS

    from .extensions import db, socketio
    from .utils.register_error_handlers import register_app_error_handlers
    from .utils.router import register_routes

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
    app.config["SECRET_KEY"] = "your_secret_key"

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)
    socketio.init_app(app)

    register_routes(app)
    register_app_error_handlers(app)

    return app
