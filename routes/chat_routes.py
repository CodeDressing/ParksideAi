"""
ParksideAI Chat Routes
Phase 3 Upgrade

Responsibilities:
- Accept guest chat messages.
- Validate and normalize payloads.
- Analyze guest intent without collecting personal information.
- Generate AI response using official Parkside routing rules.
- Return metadata for frontend UI and diagnostics.
- Provide health and diagnostics endpoints for Render/debugging.

Privacy rule:
ParksideAI does not take reservations.
ParksideAI does not collect or store guest personal information.
ParksideAI routes guests to official Parkside Tavern links.
"""

from datetime import datetime
from typing import Any, Dict, List

from flask import Blueprint, request, jsonify
from app import limiter

from services.lead_service import (
    OFFICIAL_LINKS,
    PRIVACY_MODE,
    analyze_guest_intent,
    get_quick_action_for_intent,
)
from services.openai_service import (
    generate_chat_response,
    get_openai_service_status,
)


chat_bp = Blueprint("chat", __name__)


# ============================================================
# 1. CONSTANTS
# ============================================================

MAX_MESSAGE_LENGTH = 1200
MAX_HISTORY_MESSAGES = 10

DEFAULT_SESSION_ID = "anonymous_session"
DEFAULT_VISITOR_SOURCE = "website_chat"

MAIN_WEBSITE_LINK = OFFICIAL_LINKS["main_website"]
RESERVATION_LINK = OFFICIAL_LINKS["reservations"]
PRIVATE_EVENTS_LINK = OFFICIAL_LINKS["private_events"]


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def utc_now() -> str:
    return datetime.utcnow().isoformat()


def build_error_response(
    reply: str,
    error_code: str,
    status_code: int,
    metadata: Dict[str, Any] | None = None
):
    payload = {
        "success": False,
        "reply": reply,
        "error_code": error_code,
        "metadata": metadata or {}
    }

    return jsonify(payload), status_code


def sanitize_user_message(raw_message: Any) -> str:
    if raw_message is None:
        return ""

    message = str(raw_message).strip()

    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]

    return message


def sanitize_conversation_history(raw_history: Any) -> List[Dict[str, str]]:
    if not isinstance(raw_history, list):
        return []

    cleaned_history = []

    for item in raw_history:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not isinstance(content, str) or not content.strip():
            continue

        cleaned_history.append({
            "role": role,
            "content": content.strip()[:MAX_MESSAGE_LENGTH]
        })

    return cleaned_history[-MAX_HISTORY_MESSAGES:]


def sanitize_session_id(raw_session_id: Any) -> str:
    if not raw_session_id:
        return DEFAULT_SESSION_ID

    session_id = str(raw_session_id).strip()

    if not session_id:
        return DEFAULT_SESSION_ID

    return session_id[:100]


def sanitize_page_url(raw_page_url: Any) -> str:
    if not raw_page_url:
        return ""

    return str(raw_page_url).strip()[:500]


def sanitize_visitor_source(raw_visitor_source: Any) -> str:
    if not raw_visitor_source:
        return DEFAULT_VISITOR_SOURCE

    visitor_source = str(raw_visitor_source).strip()

    if not visitor_source:
        return DEFAULT_VISITOR_SOURCE

    return visitor_source[:100]


def build_response_metadata(
    session_id: str,
    page_url: str,
    visitor_source: str,
    intent_analysis: Dict[str, Any],
    request_started_at: str
) -> Dict[str, Any]:
    quick_action = get_quick_action_for_intent(intent_analysis)

    return {
        "session_id": session_id,
        "intent": intent_analysis.get("intent", "general"),
        "guest_facing_label": intent_analysis.get(
            "guest_facing_label",
            "General Information"
        ),
        "matched_keywords": intent_analysis.get("matched_keywords", []),
        "recommended_action": intent_analysis.get(
            "recommended_action",
            "answer_and_offer_official_website"
        ),
        "official_link": intent_analysis.get(
            "official_link",
            MAIN_WEBSITE_LINK
        ),
        "priority": intent_analysis.get("priority", "normal"),
        "quick_action": quick_action,
        "page_url": page_url,
        "visitor_source": visitor_source,
        "privacy_mode": PRIVACY_MODE,
        "routing_policy": {
            "reservations": RESERVATION_LINK,
            "private_events": PRIVATE_EVENTS_LINK,
            "general_information": MAIN_WEBSITE_LINK,
        },
        "request_started_at": request_started_at,
        "request_completed_at": utc_now()
    }


# ============================================================
# 3. MAIN CHAT ENDPOINT
# ============================================================

@chat_bp.route("/", methods=["POST"])
@limiter.limit("30 per minute")
def chat():
    """
    Main guest-facing chat endpoint.
    """

    request_started_at = utc_now()

    data = request.get_json(silent=True)

    if not data:
        return build_error_response(
            reply=(
                "I did not receive a valid message. "
                f"For official Parkside Tavern information, please visit {MAIN_WEBSITE_LINK}"
            ),
            error_code="invalid_json",
            status_code=400,
            metadata={
                "request_started_at": request_started_at,
                "privacy_mode": PRIVACY_MODE
            }
        )

    user_message = sanitize_user_message(data.get("message"))
    conversation_history = sanitize_conversation_history(
        data.get("conversation_history", [])
    )
    session_id = sanitize_session_id(data.get("session_id"))
    page_url = sanitize_page_url(data.get("page_url"))
    visitor_source = sanitize_visitor_source(data.get("visitor_source"))

    if not user_message:
        return build_error_response(
            reply="Please type a message so I can help.",
            error_code="empty_message",
            status_code=400,
            metadata={
                "session_id": session_id,
                "request_started_at": request_started_at,
                "privacy_mode": PRIVACY_MODE
            }
        )

    try:
        intent_analysis = analyze_guest_intent(user_message)

        reply = generate_chat_response(
            user_message=user_message,
            conversation_history=conversation_history
        )

        metadata = build_response_metadata(
            session_id=session_id,
            page_url=page_url,
            visitor_source=visitor_source,
            intent_analysis=intent_analysis,
            request_started_at=request_started_at
        )

        return jsonify({
            "success": True,
            "reply": reply,
            "metadata": metadata
        })

    except Exception as error:
        print("CHAT ROUTE ERROR:", error)

        return build_error_response(
            reply=(
                "Something went wrong while processing your message. "
                f"For official Parkside Tavern information, please visit {MAIN_WEBSITE_LINK}"
            ),
            error_code="chat_processing_error",
            status_code=500,
            metadata={
                "session_id": session_id,
                "request_started_at": request_started_at,
                "privacy_mode": PRIVACY_MODE,
                "routing_policy": {
                    "reservations": RESERVATION_LINK,
                    "private_events": PRIVATE_EVENTS_LINK,
                    "general_information": MAIN_WEBSITE_LINK,
                }
            }
        )


# ============================================================
# 4. CHAT HEALTH ENDPOINT
# ============================================================

@chat_bp.route("/health", methods=["GET"])
def chat_health():
    return jsonify({
        "success": True,
        "service": "ParksideAI Chat",
        "status": "online",
        "privacy_mode": PRIVACY_MODE,
        "official_links": {
            "main_website": MAIN_WEBSITE_LINK,
            "reservations": RESERVATION_LINK,
            "private_events": PRIVATE_EVENTS_LINK,
        },
        "timestamp": utc_now()
    })


# ============================================================
# 5. CHAT DIAGNOSTICS ENDPOINT
# ============================================================

@chat_bp.route("/diagnostics", methods=["GET"])
def chat_diagnostics():
    """
    Non-secret diagnostics for development and Render debugging.
    Does not expose API keys or private data.
    """

    return jsonify({
        "success": True,
        "service": "ParksideAI Chat Diagnostics",
        "chat_route": {
            "status": "online",
            "max_message_length": MAX_MESSAGE_LENGTH,
            "max_history_messages": MAX_HISTORY_MESSAGES,
        },
        "openai_service": get_openai_service_status(),
        "privacy_mode": PRIVACY_MODE,
        "official_links": {
            "main_website": MAIN_WEBSITE_LINK,
            "reservations": RESERVATION_LINK,
            "private_events": PRIVATE_EVENTS_LINK,
        },
        "timestamp": utc_now()
    })


# ============================================================
# 6. ROUTING PREVIEW ENDPOINT
# ============================================================

@chat_bp.route("/route-preview", methods=["POST"])
def route_preview():
    """
    Debug endpoint to preview intent routing without calling OpenAI.
    Useful for testing:
    - reservation detection
    - private event routing
    - menu/hours/general routing
    """

    data = request.get_json(silent=True)

    if not data:
        return build_error_response(
            reply="Invalid request.",
            error_code="invalid_json",
            status_code=400,
            metadata={
                "privacy_mode": PRIVACY_MODE
            }
        )

    user_message = sanitize_user_message(data.get("message"))

    if not user_message:
        return build_error_response(
            reply="Please provide a message to preview routing.",
            error_code="empty_message",
            status_code=400,
            metadata={
                "privacy_mode": PRIVACY_MODE
            }
        )

    intent_analysis = analyze_guest_intent(user_message)
    quick_action = get_quick_action_for_intent(intent_analysis)

    return jsonify({
        "success": True,
        "message": user_message,
        "intent_analysis": intent_analysis,
        "quick_action": quick_action,
        "privacy_mode": PRIVACY_MODE,
        "timestamp": utc_now()
    })