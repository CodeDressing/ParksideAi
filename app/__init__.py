"""
============================================================
ParksideAI Application Factory
Phase 6 Part 3.0
============================================================

Responsibilities:
- create Flask application instance
- configure templates and static assets
- load production settings
- initialize rate limiting
- register application blueprints
- register search engine infrastructure
- expose health checks
============================================================
"""

# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# ============================================================
# SECTION 2 — GLOBAL EXTENSIONS
# ============================================================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        "200 per day",
        "50 per hour"
    ]
)


# ============================================================
# SECTION 3 — APPLICATION FACTORY
# ============================================================

def create_app():
    """
    Application factory for ParksideAI.
    """

    # --------------------------------------------------------
    # SUBSECTION 3.1 — BASE DIRECTORY
    # --------------------------------------------------------

    base_dir = os.path.abspath(
        os.path.dirname(__file__)
    )

    # --------------------------------------------------------
    # SUBSECTION 3.2 — FLASK APP SETUP
    # --------------------------------------------------------

    app = Flask(
        __name__,
        template_folder=os.path.join(
            base_dir,
            "..",
            "templates"
        ),
        static_folder=os.path.join(
            base_dir,
            "..",
            "static"
        ),
        static_url_path="/static"
    )

    # --------------------------------------------------------
    # SUBSECTION 3.3 — CONFIGURATION
    # --------------------------------------------------------

    from config.settings import settings

    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["APP_NAME"] = settings.APP_NAME
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

    # --------------------------------------------------------
    # SUBSECTION 3.4 — EXTENSION INITIALIZATION
    # --------------------------------------------------------

    limiter.init_app(app)

    # --------------------------------------------------------
    # SUBSECTION 3.5 — BLUEPRINT IMPORTS
    # --------------------------------------------------------

    from routes.main_routes import main_bp
    from routes.chat_routes import chat_bp
    from routes.seo_routes import seo_bp
    from routes.search_engine_routes import search_engine_bp

    # --------------------------------------------------------
    # SUBSECTION 3.6 — BLUEPRINT REGISTRATION
    # --------------------------------------------------------

    app.register_blueprint(
        main_bp
    )

    app.register_blueprint(
        chat_bp,
        url_prefix="/chat"
    )

    app.register_blueprint(
        seo_bp,
        url_prefix="/seo"
    )

    app.register_blueprint(
        search_engine_bp
    )

    # --------------------------------------------------------
    # SUBSECTION 3.7 — HEALTH CHECK
    # --------------------------------------------------------

    @app.route("/health")
    def health():
        """
        General production health check.
        """

        return {

            "status":
                "healthy",

            "app":
                settings.APP_NAME,

            "privacy_mode":
                "no_guest_data_collection",

            "search_engine_routes":
                "registered"
        }

    # --------------------------------------------------------
    # SUBSECTION 3.8 — RETURN APP
    # --------------------------------------------------------

    return app