"""
Main Routes - Landing Page
Phase 3
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Render the main ParksideAI landing page"""
    return render_template("index.html")


@main_bp.route("/privacy")
def privacy():
    """Privacy policy page"""
    return render_template("privacy.html")  # You can create this later


@main_bp.route("/terms")
def terms():
    """Terms of service page"""
    return render_template("terms.html")  # You can create this later