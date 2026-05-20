from flask import Flask
from routes.main_routes import main_bp
from routes.chat_routes import chat_bp
from routes.seo_routes import seo_bp

from config.settings import settings

import os


def create_app():

    base_dir = os.path.abspath(os.path.dirname(__file__))

    template_dir = os.path.join(base_dir, "..", "templates")
    static_dir = os.path.join(base_dir, "..", "static")

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path="/static"
    )

    # ============================================================
    # CONFIGURATION
    # ============================================================

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "parkside-development-key"
    )

    app.config["APP_NAME"] = settings.APP_NAME

    # ============================================================
    # REGISTER BLUEPRINTS
    # ============================================================

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(seo_bp, url_prefix="/seo")

    # ============================================================
    # HEALTH CHECK ROUTE
    # ============================================================

    @app.route("/health")
    def health():
        return {
            "status": "healthy",
            "app": settings.APP_NAME
        }

    return app