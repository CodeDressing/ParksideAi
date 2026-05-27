from app import create_app
from routes.search_engine_routes import search_engine_bp
app = create_app()

if __name__ == "__main__":
    app.run()
    app.register_blueprint(search_engine_bp)