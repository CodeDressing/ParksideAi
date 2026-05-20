from datetime import datetime

from flask import Blueprint, request, jsonify

from services.openai_service import generate_chat_response
from services.lead_service import analyze_guest_intent


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/", methods=["POST"])
def chat():
    """
    ParksideAI production chat endpoint.

    Current platform rule:
    - Do not take reservations directly.
    - Do not collect or store guest personal information.
    - Route guests to official Parkside Tavern links.
    """

    request_started_at = datetime.utcnow().isoformat()

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "reply": "I did not receive a valid message.",
            "error_code": "invalid_json",
            "metadata": {
                "request_started_at": request_started_at
            }
        }), 400

    user_message = str(data.get("message", "")).strip()
    conversation_history = data.get("conversation_history", [])
    session_id = data.get("session_id", "anonymous_session")
    page_url = data.get("page_url", "")
    visitor_source = data.get("visitor_source", "website_chat")

    if not user_message:
        return jsonify({
            "success": False,
            "reply": "Please type a message so I can help.",
            "error_code": "empty_message",
            "metadata": {
                "session_id": session_id,
                "request_started_at": request_started_at
            }
        }), 400

    if not isinstance(conversation_history, list):
        conversation_history = []

    try:
        intent_analysis = analyze_guest_intent(user_message)

        reply = generate_chat_response(
            user_message=user_message,
            conversation_history=conversation_history
        )

        return jsonify({
            "success": True,
            "reply": reply,
            "metadata": {
                "session_id": session_id,
                "intent": intent_analysis.get("intent", "general"),
                "matched_keywords": intent_analysis.get("matched_keywords", []),
                "recommended_action": intent_analysis.get(
                    "recommended_action",
                    "answer_and_offer_official_website"
                ),
                "official_link": intent_analysis.get(
                    "official_link",
                    "https://parksidenj.com/"
                ),
                "priority": intent_analysis.get("priority", "normal"),
                "page_url": page_url,
                "visitor_source": visitor_source,
                "privacy_mode": "no_guest_info_collection",
                "request_started_at": request_started_at,
                "request_completed_at": datetime.utcnow().isoformat()
            }
        })

    except Exception as error:
        print("CHAT ROUTE ERROR:", error)

        return jsonify({
            "success": False,
            "reply": (
                "Something went wrong while processing your message. "
                "For official Parkside Tavern information, please visit "
                "https://parksidenj.com/"
            ),
            "error_code": "chat_processing_error",
            "metadata": {
                "session_id": session_id,
                "privacy_mode": "no_guest_info_collection",
                "request_started_at": request_started_at
            }
        }), 500


@chat_bp.route("/health", methods=["GET"])
def chat_health():
    return jsonify({
        "success": True,
        "service": "ParksideAI Chat",
        "status": "online",
        "privacy_mode": "no_guest_info_collection",
        "timestamp": datetime.utcnow().isoformat()
    })