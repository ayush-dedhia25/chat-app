from flask import Flask


def register_routes(app: Flask):
    """
    Register routes for the chat application.

    This function registers the routes for the chat application. It imports
    the routes for the chats and auth blueprints and registers them with the
    app.

    Args:
        app (Flask): The Flask app to register the routes with
    """
    from ..routes import chats as chats_blueprint, auth as auth_blueprint

    app.register_blueprint(chats_blueprint)
    app.register_blueprint(auth_blueprint)
