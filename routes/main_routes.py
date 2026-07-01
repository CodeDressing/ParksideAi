"""
============================================================
ParksideAI
Main Routes Controller
Phase 5 Part 1.0
============================================================

Responsibilities:
- Homepage rendering
- Global SEO metadata
- Trust routing
- Footer data
- Official link exposure
- Public platform presentation
- Future analytics hooks
"""

# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

import hashlib
import json
from datetime import datetime
from pathlib import Path

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from config.settings import settings
# ============================================================
# SECTION 2 — BLUEPRINT SETUP
# ============================================================

main_bp = Blueprint(
    "main",
    __name__
)


# ============================================================
# SECTION 3.5 — PRIVACY-SAFE ANALYTICS CONFIG
# ============================================================

ANALYTICS_LOG_PATH = Path("data/analytics_events.jsonl")

ALLOWED_ANALYTICS_EVENTS = {
    "page_viewed",
    "time_on_page",
    "button_clicked",
    "chat_opened",
    "chat_minimized",
    "chat_message_sent",
    "opentable_clicked",
    "private_events_clicked",
    "food_menu_clicked",
    "drink_menu_clicked"
}


def utc_now():
    return datetime.utcnow().isoformat()


def get_anonymous_ip_hash():
    raw_ip = (
        request.headers.get("X-Forwarded-For", "")
        .split(",")[0]
        .strip()
        or request.remote_addr
        or "unknown"
    )

    return hashlib.sha256(raw_ip.encode("utf-8")).hexdigest()[:24]


def sanitize_analytics_text(value, max_length=500):
    if value is None:
        return ""

    return str(value).strip()[:max_length]


def write_analytics_event(event_payload):
    ANALYTICS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with ANALYTICS_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event_payload, ensure_ascii=False) + "\n")

# ============================================================
# SECTION 4 — HOMEPAGE SEO DATA
# ============================================================

HOMEPAGE_SEO_DATA = {

    "title":
        "ParksideAI | Parkside Tavern Hospitality Assistant",

    "description":
        (
            "ParksideAI helps guests discover official "
            "Parkside Tavern information including "
            "reservations, private events, menus, "
            "cocktails, brunch, happy hour, and "
            "Morristown restaurant details."
        ),

    "keywords": [

        "Parkside Tavern",
        "ParksideAI",
        "Morristown restaurant",
        "Morristown tavern",
        "Morristown cocktails",
        "Morristown brunch",
        "private events Morristown",
        "Parkside Tavern reservations",
        "Morristown nightlife",
        "Morristown dining"
    ],

    "canonical":
        settings.OFFICIAL_MAIN_WEBSITE
}


# ============================================================
# SECTION 5 — HOMEPAGE FEATURE CARDS
# ============================================================

HOMEPAGE_FEATURE_CARDS = [

    {
        "title":
            "Reservations",

        "description":
            (
                "Use the official OpenTable page "
                "for Parkside Tavern reservations."
            ),

        "url":
            settings.OFFICIAL_RESERVATION_LINK,

        "button":
            "Book on OpenTable"
    },

    {
        "title":
            "Private Events",

        "description":
            (
                "Submit official inquiries for "
                "parties, celebrations, and "
                "group gatherings."
            ),

        "url":
            settings.OFFICIAL_PRIVATE_EVENTS_LINK,

        "button":
            "Event Inquiry"
    },

    {
        "title":
            "Food Menu",

        "description":
            (
                "Explore Parkside Tavern food "
                "offerings and dining information."
            ),

        "url":
            settings.OFFICIAL_FOOD_MENU_LINK,

        "button":
            "View Menu"
    },

    {
        "title":
            "Drink Menu",

        "description":
            (
                "Explore cocktails, spirits, wine, "
                "beer, and bar offerings."
            ),

        "url":
            settings.OFFICIAL_DRINK_MENU_LINK,

        "button":
            "View Drinks"
    }
]


# ============================================================
# SECTION 6 — SEO PAGE PREVIEW CARDS
# ============================================================

SEO_PREVIEW_CARDS = [

    {
        "title":
            "Private Events",

        "url":
            "/seo/private-events",

        "description":
            (
                "Morristown private event discovery "
                "and hospitality routing."
            )
    },

    {
        "title":
            "Birthday Parties",

        "url":
            "/seo/birthday-parties",

        "description":
            (
                "Birthday celebrations and group "
                "dining discovery."
            )
    },

    {
        "title":
            "Corporate Events",

        "url":
            "/seo/corporate-events",

        "description":
            (
                "Business dinners and corporate "
                "gathering routing."
            )
    },

    {
        "title":
            "Holiday Parties",

        "url":
            "/seo/holiday-parties",

        "description":
            (
                "Holiday hospitality and event "
                "discovery pages."
            )
    },

    {
        "title":
            "Brunch",

        "url":
            "/seo/brunch",

        "description":
            (
                "Brunch discovery for Morristown "
                "restaurant guests."
            )
    },

    {
        "title":
            "Cocktails",

        "url":
            "/seo/cocktails",

        "description":
            (
                "Cocktail bar discovery and "
                "drink menu routing."
            )
    }
]


# ============================================================
# SECTION 7 — TRUST / PRIVACY DATA
# ============================================================

TRUST_DATA = [

    {
        "title":
            "Official Reservation Routing",

        "description":
            (
                "ParksideAI routes reservation "
                "guests directly to OpenTable."
            )
    },

    {
        "title":
            "No Guest Data Collection",

        "description":
            (
                "ParksideAI does not collect "
                "names, phone numbers, emails, "
                "or payment information."
            )
    },

    {
        "title":
            "Official Information First",

        "description":
            (
                "Restaurant information is "
                "sourced from official "
                "Parkside Tavern platforms."
            )
    }
]


# ============================================================
# SECTION 8 — FOOTER DATA
# ============================================================

FOOTER_LINKS = [

    {
        "label":
            "Official Website",

        "url":
            settings.OFFICIAL_MAIN_WEBSITE
    },

    {
        "label":
            "Reservations",

        "url":
            settings.OFFICIAL_RESERVATION_LINK
    },

    {
        "label":
            "Private Events",

        "url":
            settings.OFFICIAL_PRIVATE_EVENTS_LINK
    }
]


# ============================================================
# SECTION 9 — MAIN HOMEPAGE
# ============================================================

@main_bp.route("/")
def home():
    """
    Render the ParksideAI homepage.
    """

    return render_template(

        "index.html",

        platform=GLOBAL_PLATFORM_CONTEXT,

        seo=HOMEPAGE_SEO_DATA,

        feature_cards=HOMEPAGE_FEATURE_CARDS,

        seo_cards=SEO_PREVIEW_CARDS,

        trust_cards=TRUST_DATA,

        footer_links=FOOTER_LINKS
    )


# ============================================================
# SECTION 10 — PRIVACY PAGE
# ============================================================

@main_bp.route("/privacy")
def privacy():
    """
    Privacy policy route.
    """

    return render_template(

        "privacy.html",

        platform=GLOBAL_PLATFORM_CONTEXT
    )


# ============================================================
# SECTION 11 — TERMS PAGE
# ============================================================

@main_bp.route("/terms")
def terms():
    """
    Terms of service route.
    """

    return render_template(

        "terms.html",

        platform=GLOBAL_PLATFORM_CONTEXT
    )


# ============================================================
# SECTION 12 — HEALTH CHECK
# ============================================================

@main_bp.route("/health")
def health():
    """
    Lightweight Render health check.
    """

    return {

        "success": True,

        "platform":
            settings.APP_NAME,

        "restaurant":
            settings.RESTAURANT_NAME,

        "status":
            "online",

        "privacy_mode":
            settings.PRIVACY_MODE
    }

# ============================================================
# SECTION 13 — ANALYTICS EVENT INGESTION
# ============================================================

@main_bp.route("/analytics/event", methods=["POST"])
def analytics_event():
    """
    Privacy-safe visitor analytics endpoint.

    Tracks anonymous site behavior without collecting:
    - names
    - emails
    - phone numbers
    - payment details
    - reservation details
    - private booking details
    """

    data = request.get_json(silent=True) or {}

    event_type = sanitize_analytics_text(data.get("event_type"), 100)

    if event_type not in ALLOWED_ANALYTICS_EVENTS:
        return jsonify({
            "success": False,
            "error": "unsupported_event_type"
        }), 400

    event_payload = {
        "event_type": event_type,
        "timestamp": utc_now(),
        "anonymous_session_id": sanitize_analytics_text(
            data.get("anonymous_session_id"),
            120
        ),
        "page_url": sanitize_analytics_text(
            data.get("page_url"),
            500
        ),
        "page_title": sanitize_analytics_text(
            data.get("page_title"),
            200
        ),
        "referrer": sanitize_analytics_text(
            data.get("referrer"),
            500
        ),
        "device": {
            "user_agent": sanitize_analytics_text(
                request.headers.get("User-Agent"),
                500
            ),
            "browser_language": sanitize_analytics_text(
                data.get("browser_language"),
                80
            ),
            "screen_width": data.get("screen_width"),
            "screen_height": data.get("screen_height")
        },
        "engagement": {
            "time_on_page_seconds": data.get("time_on_page_seconds"),
            "button_label": sanitize_analytics_text(
                data.get("button_label"),
                120
            ),
            "button_url": sanitize_analytics_text(
                data.get("button_url"),
                500
            )
        },
        "privacy": {
            "raw_ip_stored": False,
            "anonymous_ip_hash": get_anonymous_ip_hash(),
            "personal_information_collected": False
        }
    }

    write_analytics_event(event_payload)

    return jsonify({
        "success": True,
        "event_type": event_type
    })


# ============================================================
# SECTION 14 — ANALYTICS HEALTH CHECK
# ============================================================

@main_bp.route("/analytics/health")
def analytics_health():
    """
    Analytics system health check.
    """

    return jsonify({
        "success": True,
        "service": "ParksideAI Privacy-Safe Analytics",
        "status": "online",
        "log_path": str(ANALYTICS_LOG_PATH),
        "allowed_events": sorted(ALLOWED_ANALYTICS_EVENTS),
        "privacy_mode": {
            "raw_ip_stored": False,
            "personal_information_collected": False
        },
        "timestamp": utc_now()
    })