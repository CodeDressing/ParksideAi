"""
ParksideAI SEO Routes
Phase 4 Upgrade

Responsibilities:
- Serve SEO engine status
- List available SEO landing pages
- Render dynamic local SEO landing pages
- Provide JSON SEO data endpoints
- Route users to official Parkside Tavern links
- Avoid collecting guest information
- Avoid taking reservations directly
"""

import json

from flask import Blueprint, jsonify, render_template

from config.settings import settings
from services.seo_service import seo_service


seo_bp = Blueprint("seo", __name__, url_prefix="/seo")


# ============================================================
# 1. SEO ENGINE STATUS
# ============================================================

@seo_bp.route("/", methods=["GET"])
def seo_home():
    """
    SEO engine index endpoint.

    Useful for:
    - checking Render deployment
    - inspecting available SEO pages
    - future sitemap generation
    """

    return jsonify(seo_service.build_seo_index_payload())


# ============================================================
# 2. SEO PAGE LIST API
# ============================================================

@seo_bp.route("/pages", methods=["GET"])
def seo_pages():
    """
    Return available SEO landing pages as JSON.
    """

    return jsonify({
        "success": True,
        "restaurant": settings.RESTAURANT_NAME,
        "pages": seo_service.list_available_pages(),
        "privacy_mode": settings.PRIVACY_MODE,
        "official_links": seo_service.get_official_links()
    })


# ============================================================
# 3. SEO KEYWORD CONTEXT API
# ============================================================

@seo_bp.route("/keywords", methods=["GET"])
def seo_keywords():
    """
    Return local SEO keyword context.

    This helps debug:
    - local SEO targets
    - service categories
    - semantic topics
    - official routing links
    """

    return jsonify({
        "success": True,
        "keyword_context": seo_service.generate_keyword_context(),
        "seo_rules": settings.SEO_PAGE_RULES
    })


# ============================================================
# 4. DYNAMIC SEO LANDING PAGE
# ============================================================

@seo_bp.route("/<slug>", methods=["GET"])
def seo_landing_page(slug):
    """
    Render a dynamic SEO landing page.

    Example:
    /seo/private-events
    /seo/birthday-parties
    /seo/corporate-events
    /seo/holiday-parties
    /seo/brunch
    /seo/happy-hour
    /seo/cocktails
    /seo/dinner
    /seo/sports-viewing
    /seo/group-dining
    """

    page_data = seo_service.build_landing_page(slug)

    if not page_data:
        return jsonify(
            seo_service.build_page_not_found_payload(slug)
        ), 404

    schema_json = json.dumps(
        page_data.get("schema", {}),
        indent=2
    )

    return render_template(
        "seo_page.html",
        page=page_data,
        schema_json=schema_json
    )


# ============================================================
# 5. SEO LANDING PAGE JSON API
# ============================================================

@seo_bp.route("/<slug>/json", methods=["GET"])
def seo_landing_page_json(slug):
    """
    Return SEO landing page data as JSON.

    Useful for:
    - debugging
    - future page generation
    - future AI SEO automation
    - future sitemap/feed generation
    """

    page_data = seo_service.build_landing_page(slug)

    if not page_data:
        return jsonify(
            seo_service.build_page_not_found_payload(slug)
        ), 404

    return jsonify({
        "success": True,
        "page": page_data
    })


# ============================================================
# 6. LEGACY ROUTE COMPATIBILITY
# ============================================================

@seo_bp.route("/reservations", methods=["GET"])
def seo_reservations():
    """
    SEO-friendly reservation routing page.

    This page exists so reservation-search users land on a helpful
    ParksideAI page before being directed to the official OpenTable link.
    """

    page_data = {
        "slug": "reservations",
        "title": "Reservations",
        "headline": f"Reservations at {settings.RESTAURANT_NAME} in {settings.RESTAURANT_CITY}, {settings.RESTAURANT_STATE}",
        "subheadline": (
            f"Parkside Tavern reservations are handled through OpenTable. "
            f"ParksideAI does not take reservations directly."
        ),
        "primary_keyword": "Parkside Tavern reservations",
        "meta": {
            "title": f"Parkside Tavern Reservations | Morristown NJ",
            "description": (
                "Find the official Parkside Tavern reservation link for "
                "OpenTable in Morristown, NJ."
            ),
            "canonical": settings.OFFICIAL_RESERVATION_LINK,
            "robots": "index, follow"
        },
        "content_sections": [
            {
                "heading": "Book Through OpenTable",
                "body": (
                    "Parkside Tavern reservations are handled through the official "
                    "OpenTable page. ParksideAI does not take reservations directly "
                    "or collect guest reservation information."
                )
            }
        ],
        "cta": {
            "label": "Book on OpenTable",
            "url": settings.OFFICIAL_RESERVATION_LINK,
            "type": "official_reservation_link"
        },
        "official_links": seo_service.get_official_links(),
        "privacy_note": (
            "ParksideAI does not take reservations or collect guest information."
        ),
        "schema": seo_service.build_structured_data(),
        "seo_rules": settings.SEO_PAGE_RULES
    }

    schema_json = json.dumps(page_data["schema"], indent=2)

    return render_template(
        "seo_page.html",
        page=page_data,
        schema_json=schema_json
    )


@seo_bp.route("/menu", methods=["GET"])
def seo_menu():
    """
    SEO-friendly menu routing page.
    """

    page_data = seo_service.build_landing_page("dinner")

    if not page_data:
        return jsonify(seo_service.build_page_not_found_payload("dinner")), 404

    page_data["slug"] = "menu"
    page_data["title"] = "Menu"
    page_data["headline"] = f"Parkside Tavern Menu in Morristown, NJ"
    page_data["subheadline"] = (
        "Explore Parkside Tavern food and drink information through the official website."
    )
    page_data["primary_keyword"] = "Parkside Tavern menu"
    page_data["cta"] = {
        "label": "View Food Menu",
        "url": settings.OFFICIAL_FOOD_MENU_LINK,
        "type": "official_menu_link"
    }

    schema_json = json.dumps(page_data.get("schema", {}), indent=2)

    return render_template(
        "seo_page.html",
        page=page_data,
        schema_json=schema_json
    )