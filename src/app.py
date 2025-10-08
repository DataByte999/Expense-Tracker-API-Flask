from flask import Flask

from src.exceptions import register_error_handlers
from src.routes.auth_routes import auth_bp
from src.routes.transactions_routes import tx_bp
from src.routes.users_routes import user_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(tx_bp)

    register_error_handlers(app)

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
