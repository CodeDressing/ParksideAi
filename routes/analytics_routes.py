"""
============================================================
ParksideAI Analytics Routes
File: routes/analytics_routes.py
Phase 7 Part 3.1B
Privacy-Safe Visitor Analytics Route Layer
============================================================

Responsibilities:
- Receive anonymous visitor analytics events.
- Track page views.
- Track time on page.
- Track button clicks.
- Track chat interactions.
- Track OpenTable, private event, food menu, and drink menu clicks.
- Track browser/device metadata.
- Track referrer source.
- Store only privacy-safe analytics data.

Privacy Rules:
- Do NOT collect names.
- Do NOT collect emails.
- Do NOT collect phone numbers.
- Do NOT collect payment details.
- Do NOT collect reservation details.
- Do NOT collect private booking details.
- Do NOT store raw IP addresses.
============================================================
"""

# ============================================================
# SECTION 01 — IMPORTS
# ============================================================

import hashlib
import json
from datetime import datetime
from pathlib import Path

from flask import Blueprint
from flask import jsonify
from flask import request


# ============================================================
# SECTION 02 — BLUEPRINT SETUP
# ============================================================

analytics_bp = Blueprint(
    "analytics",
    __name__
)


# ============================================================
# SECTION 03 — ANALYTICS CONFIGURATION
# ============================================================

ANALYTICS_LOG_PATH = Path("data/analytics_events.jsonl")

ALLOWED_EVENTS = {
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


# ============================================================
# SECTION 04 — UTILITY HELPERS
# ============================================================

def utc_now():
    return datetime.utcnow().isoformat()


def sanitize_text(value, max_length=500):
    if value is None:
        return ""

    return str(value).strip()[:max_length]


def anonymous_ip_hash():
    raw_ip = (
        request.headers.get("X-Forwarded-For", "")
        .split(",")[0]
        .strip()
        or request.remote_addr
        or "unknown"
    )

    return hashlib.sha256(
        raw_ip.encode("utf-8")
    ).hexdigest()[:24]


def write_event(event_payload):
    ANALYTICS_LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with ANALYTICS_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(event_payload, ensure_ascii=False) + "\n"
        )


# ============================================================
# SECTION 05 — ANALYTICS EVENT INGESTION
# ============================================================

@analytics_bp.route("/event", methods=["POST"])
def analytics_event():
    data = request.get_json(silent=True) or {}

    event_type = sanitize_text(
        data.get("event_type"),
        100
    )

    if event_type not in ALLOWED_EVENTS:
        return jsonify({
            "success": False,
            "error": "unsupported_event_type",
            "event_type": event_type
        }), 400

    event_payload = {
        "event_type": event_type,
        "timestamp": utc_now(),
        "anonymous_session_id": sanitize_text(
            data.get("anonymous_session_id"),
            120
        ),
        "page": {
            "url": sanitize_text(
                data.get("page_url"),
                500
            ),
            "title": sanitize_text(
                data.get("page_title"),
                200
            ),
            "referrer": sanitize_text(
                data.get("referrer"),
                500
            )
        },
        "device": {
            "user_agent": sanitize_text(
                request.headers.get("User-Agent"),
                500
            ),
            "browser_language": sanitize_text(
                data.get("browser_language"),
                80
            ),
            "screen_width": data.get("screen_width"),
            "screen_height": data.get("screen_height")
        },
        "engagement": {
            "time_on_page_seconds": data.get("time_on_page_seconds"),
            "button_label": sanitize_text(
                data.get("button_label"),
                120
            ),
            "button_url": sanitize_text(
                data.get("button_url"),
                500
            )
        },
        "privacy": {
            "raw_ip_stored": False,
            "anonymous_ip_hash": anonymous_ip_hash(),
            "personal_information_collected": False
        }
    }

    write_event(event_payload)

    return jsonify({
        "success": True,
        "event_type": event_type
    })


# ============================================================
# SECTION 06 — ANALYTICS HEALTH CHECK
# ============================================================

@analytics_bp.route("/health", methods=["GET"])
def analytics_health():
    return jsonify({
        "success": True,
        "service": "ParksideAI Privacy-Safe Analytics",
        "status": "online",
        "log_path": str(ANALYTICS_LOG_PATH),
        "allowed_events": sorted(ALLOWED_EVENTS),
        "privacy_mode": {
            "raw_ip_stored": False,
            "personal_information_collected": False
        },
        "timestamp": utc_now()
    })