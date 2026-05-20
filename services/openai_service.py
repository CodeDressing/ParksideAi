import json
from pathlib import Path

from openai import OpenAI

from config.settings import settings
from parkside_chatbot.prompts import build_messages
from services.lead_service import analyze_guest_intent, build_routing_instruction


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def load_restaurant_knowledge():
    knowledge_path = Path(settings.KNOWLEDGE_FILE)

    if not knowledge_path.exists():
        return ""

    try:
        with open(knowledge_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return json.dumps(data, indent=2)

    except Exception as error:
        print("KNOWLEDGE LOAD ERROR:", error)
        return ""


def generate_chat_response(user_message, conversation_history=None):
    if not user_message or not user_message.strip():
        return "Please send me a message so I can help."

    if not settings.OPENAI_API_KEY:
        return "OpenAI API key is missing. Please check the environment variables."

    restaurant_context = load_restaurant_knowledge()
    intent_analysis = analyze_guest_intent(user_message)
    routing_instruction = build_routing_instruction(intent_analysis)

    safety_instruction = """
Important platform rule:
ParksideAI does not take reservations directly.
ParksideAI does not collect or store guest personal information.
Do not ask for names, phone numbers, emails, or private guest details.
Instead, guide guests to the correct official Parkside Tavern link.

Official routing:
- Main website: https://parksidenj.com/
- Reservations: https://www.opentable.com/r/parkside-tavern-morristown
- Private events: https://parksidetavern.tripleseat.com/party_request/45075
"""

    full_context = f"""
{restaurant_context}

Guest intent routing instruction:
{routing_instruction}

{safety_instruction}
"""

    messages = build_messages(
        user_message=user_message,
        restaurant_context=full_context,
        conversation_history=conversation_history
    )

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
        )

        return response.choices[0].message.content

    except Exception as error:
        print("OPENAI SERVICE ERROR:", error)

        return (
            "I’m having trouble connecting to the AI system right now, "
            "but you can visit the official Parkside Tavern website here: "
            "https://parksidenj.com/"
        )