from flask import Blueprint, request, jsonify
from services.openai_service import generate_chat_response

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = generate_chat_response(user_message)

    return jsonify({
        "reply": response
    })