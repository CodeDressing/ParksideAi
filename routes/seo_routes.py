from flask import Blueprint, jsonify

seo_bp = Blueprint("seo", __name__)


@seo_bp.route("/")
def seo_home():
    return jsonify({
        "message": "ParksideAI SEO engine is online."
    })