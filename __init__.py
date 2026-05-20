from flask import Flask
from routes.main_routes import main_bp
from routes.chat_routes import chat_bp
from routes.seo_routes import seo_bp
import os


def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "..", "templates"),
        static_folder=os.path.join(base_dir, "..", "static"),
        static_url_path="/static"
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(seo_bp, url_prefix="/seo")

    return app