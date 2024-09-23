from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    from flask import Flask
    from flask_cors import CORS

    from config import Config as AppConfig

    from .extensions import db, socketio
    from .utils.register_error_handlers import register_app_error_handlers
    from .utils.router import register_routes

    app = Flask(__name__)
    app.config.from_object(AppConfig)

    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
    )

    db.init_app(app)
    socketio.init_app(app)

    register_routes(app)
    register_app_error_handlers(app)

    return app
