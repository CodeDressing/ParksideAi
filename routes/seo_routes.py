"""
============================================================
ParksideAI
SEO Routes Controller
Phase 5 Part 1.0
============================================================

Responsibilities:
- SEO landing page rendering
- SEO discovery index
- structured navigation
- sitemap readiness
- semantic SEO routing
- local hospitality discovery
- official Parkside Tavern routing
"""

# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

import json

from flask import Blueprint
from flask import jsonify
from flask import render_template

from config.settings import settings
from services.seo_service import seo_service


# ============================================================
# SECTION 2 — BLUEPRINT SETUP
# ============================================================

seo_bp = Blueprint(
    "seo",
    __name__,
    url_prefix="/seo"
)


# ============================================================
# SECTION 3 — SEO DISCOVERY INDEX
# ============================================================

SEO_DISCOVERY_GROUPS = [

    {
        "category":
            "Events",

        "pages": [

            "private-events",
            "birthday-parties",
            "corporate-events",
            "holiday-parties",
            "group-dining"
        ]
    },

    {
        "category":
            "Dining",

        "pages": [

            "brunch",
            "dinner",
            "happy-hour",
            "cocktails"
        ]
    },

    {
        "category":
            "Hospitality",

        "pages": [

            "sports-viewing"
        ]
    }
]


# ============================================================
# SECTION 4 — SEO ENGINE STATUS
# ============================================================

@seo_bp.route("/", methods=["GET"])
def seo_home():
    """
    Public SEO discovery index.
    """

    available_pages = (
        seo_service.list_available_pages()
    )

    return render_template(

        "seo_page.html",

        seo_groups=
            SEO_DISCOVERY_GROUPS,

        available_pages=
            available_pages,

        official_links=
            seo_service.get_official_links(),

        restaurant=
            settings.RESTAURANT_NAME,

        city=
            settings.RESTAURANT_CITY,

        state=
            settings.RESTAURANT_STATE
    )


# ============================================================
# SECTION 5 — SEO PAGE API
# ============================================================

@seo_bp.route("/pages", methods=["GET"])
def seo_pages():
    """
    Return SEO pages as JSON.
    """

    return jsonify({

        "success": True,

        "restaurant":
            settings.RESTAURANT_NAME,

        "pages":
            seo_service.list_available_pages(),

        "privacy_mode":
            settings.PRIVACY_MODE,

        "official_links":
            seo_service.get_official_links()
    })


# ============================================================
# SECTION 6 — SEO KEYWORD API
# ============================================================

@seo_bp.route("/keywords", methods=["GET"])
def seo_keywords():
    """
    Keyword context endpoint.
    """

    return jsonify({

        "success": True,

        "keyword_context":
            seo_service.generate_keyword_context(),

        "seo_rules":
            settings.SEO_PAGE_RULES
    })


# ============================================================
# SECTION 7 — DYNAMIC SEO LANDING PAGE
# ============================================================

@seo_bp.route("/<slug>", methods=["GET"])
def seo_landing_page(slug):
    """
    Dynamic SEO landing page renderer.
    """

    page_data = (
        seo_service.build_landing_page(slug)
    )

    if not page_data:

        return jsonify(

            seo_service.build_page_not_found_payload(
                slug
            )

        ), 404

    schema_json = json.dumps(

        page_data.get(
            "schema",
            {}
        ),

        indent=2
    )

    related_pages = (
        seo_service.get_related_pages(slug)
    )

    return render_template(

        "seo_page.html",

        page=
            page_data,

        schema_json=
            schema_json,

        related_pages=
            related_pages,

        official_links=
            seo_service.get_official_links()
    )


# ============================================================
# SECTION 8 — SEO LANDING PAGE JSON
# ============================================================

@seo_bp.route("/<slug>/json", methods=["GET"])
def seo_landing_page_json(slug):
    """
    JSON SEO payload endpoint.
    """

    page_data = (
        seo_service.build_landing_page(slug)
    )

    if not page_data:

        return jsonify(

            seo_service.build_page_not_found_payload(
                slug
            )

        ), 404

    return jsonify({

        "success": True,

        "page":
            page_data,

        "related_pages":
            seo_service.get_related_pages(slug)
    })


# ============================================================
# SECTION 9 — SEO SITEMAP PREVIEW
# ============================================================

@seo_bp.route("/sitemap-preview", methods=["GET"])
def sitemap_preview():
    """
    Lightweight sitemap preview endpoint.
    """

    pages = (
        seo_service.list_available_pages()
    )

    sitemap_urls = []

    for page in pages:

        sitemap_urls.append({

            "slug":
                page["slug"],

            "url":
                f"/seo/{page['slug']}"
        })

    return jsonify({

        "success": True,

        "pages":
            sitemap_urls
    })


# ============================================================
# SECTION 10 — RESERVATION LANDING PAGE
# ============================================================

@seo_bp.route("/reservations", methods=["GET"])
def seo_reservations():
    """
    Reservation SEO landing page.
    """

    page_data = {

        "slug":
            "reservations",

        "title":
            "Reservations",

        "headline":
            (
                f"Reservations at "
                f"{settings.RESTAURANT_NAME}"
            ),

        "subheadline":
            (
                "Parkside Tavern reservations "
                "are handled through the official "
                "OpenTable platform."
            ),

        "primary_keyword":
            "Parkside Tavern reservations",

        "meta": {

            "title":
                (
                    "Parkside Tavern Reservations "
                    "| Morristown NJ"
                ),

            "description":
                (
                    "Find the official reservation "
                    "platform for Parkside Tavern."
                ),

            "canonical":
                settings.OFFICIAL_RESERVATION_LINK,

            "robots":
                "index, follow"
        },

        "content_sections": [

            {
                "heading":
                    "Book Through OpenTable",

                "body":
                    (
                        "Reservations are routed "
                        "through OpenTable. "
                        "ParksideAI does not take "
                        "reservations directly."
                    )
            }
        ],

        "cta": {

            "label":
                "Book on OpenTable",

            "url":
                settings.OFFICIAL_RESERVATION_LINK,

            "type":
                "official_reservation_link"
        },

        "official_links":
            seo_service.get_official_links(),

        "privacy_note":
            (
                "ParksideAI does not collect "
                "guest reservation information."
            ),

        "schema":
            seo_service.build_structured_data(),

        "seo_rules":
            settings.SEO_PAGE_RULES
    }

    schema_json = json.dumps(

        page_data["schema"],
        indent=2
    )

    return render_template(

        "seo_page.html",

        page=
            page_data,

        schema_json=
            schema_json,

        related_pages=
            seo_service.get_related_pages(
                "private-events"
            ),

        official_links=
            seo_service.get_official_links()
    )


# ============================================================
# SECTION 11 — MENU LANDING PAGE
# ============================================================

@seo_bp.route("/menu", methods=["GET"])
def seo_menu():
    """
    SEO menu landing page.
    """

    page_data = (
        seo_service.build_landing_page(
            "dinner"
        )
    )

    if not page_data:

        return jsonify(

            seo_service.build_page_not_found_payload(
                "dinner"
            )

        ), 404

    page_data["slug"] = "menu"

    page_data["title"] = "Menu"

    page_data["headline"] = (
        "Parkside Tavern Menu "
        "in Morristown NJ"
    )

    page_data["subheadline"] = (
        "Explore official food and drink "
        "information through Parkside Tavern."
    )

    page_data["primary_keyword"] = (
        "Parkside Tavern menu"
    )

    page_data["cta"] = {

        "label":
            "View Food Menu",

        "url":
            settings.OFFICIAL_FOOD_MENU_LINK,

        "type":
            "official_menu_link"
    }

    schema_json = json.dumps(

        page_data.get(
            "schema",
            {}
        ),

        indent=2
    )

    return render_template(

        "seo_page.html",

        page=
            page_data,

        schema_json=
            schema_json,

        related_pages=
            seo_service.get_related_pages(
                "dinner"
            ),

        official_links=
            seo_service.get_official_links()
    )


# ============================================================
# SECTION 12 — SEO HEALTH CHECK
# ============================================================

@seo_bp.route("/health", methods=["GET"])
def seo_health():
    """
    SEO engine health check.
    """

    return {

        "success": True,

        "engine":
            "ParksideAI SEO Engine",

        "restaurant":
            settings.RESTAURANT_NAME,

        "status":
            "online",

        "seo_pages":
            len(
                seo_service.list_available_pages()
            )
    }