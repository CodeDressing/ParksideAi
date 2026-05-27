# ============================================================
# ParksideAI
# Application Entry Point
# Phase 5 Part 2.6
# ============================================================

from app import create_app

from routes.search_engine_routes import search_engine_bp


# ============================================================
# SECTION 1 — APP FACTORY
# ============================================================

app = create_app()


# ============================================================
# SECTION 2 — SEARCH ENGINE BLUEPRINT REGISTRATION
# ============================================================

app.register_blueprint(
    search_engine_bp
)


# ============================================================
# SECTION 3 — LOCAL DEVELOPMENT SERVER
# ============================================================

if __name__ == "__main__":

    app.run()