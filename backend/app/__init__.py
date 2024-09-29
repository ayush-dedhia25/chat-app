from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    from flask import Flask
    from flask_cors import CORS

    from config import Config as AppConfig

    from .extensions import db
    from .socket_events import socketio
    from .utils.register_error_handlers import register_app_error_handlers
    from .utils.router import register_routes

    app = Flask(__name__)
    app.config.from_object(AppConfig)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="http://localhost:5173")

    register_routes(app)
    register_app_error_handlers(app)

    return app
