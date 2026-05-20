"""
ParksideAI Application Factory
Phase 3 - Production Ready
"""

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Initialize rate limiter (will be configured with app)
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])


def create_app():
    """Application factory for ParksideAI"""

    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "..", "templates"),
        static_folder=os.path.join(base_dir, "..", "static"),
        static_url_path="/static"
    )

    # Load configuration
    from config.settings import settings
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["APP_NAME"] = settings.APP_NAME
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # 1MB max request size

    # Initialize rate limiter with app
    limiter.init_app(app)

    # Register blueprints
    from routes.main_routes import main_bp
    from routes.chat_routes import chat_bp
    from routes.seo_routes import seo_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(seo_bp, url_prefix="/seo")

    # Health check endpoint
    @app.route("/health")
    def health():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "privacy_mode": "no_guest_data_collection"
        }

    return app