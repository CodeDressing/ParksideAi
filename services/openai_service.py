"""
ParksideAI OpenAI Service
Phase 3 Upgrade

Responsibilities:
- Load official Parkside Tavern knowledge.
- Analyze guest intent.
- Inject official routing instructions.
- Call OpenAI safely.
- Never crash the Flask app if the API key is missing.
- Never collect guest information.
- Never take reservations directly.
- Route reservations to OpenTable.
- Route private events to Tripleseat.
- Route general information to parksidenj.com.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from openai import OpenAI

from config.settings import settings
from parkside_chatbot.prompts import build_messages
from services.lead_service import (
    OFFICIAL_LINKS,
    analyze_guest_intent,
    build_routing_instruction,
)


# ============================================================
# 1. SERVICE CONSTANTS
# ============================================================

MAIN_WEBSITE_LINK = OFFICIAL_LINKS["main_website"]
RESERVATION_LINK = OFFICIAL_LINKS["reservations"]
PRIVATE_EVENTS_LINK = OFFICIAL_LINKS["private_events"]

SAFE_FALLBACK_MESSAGE = (
    "I’m having trouble connecting to the AI system right now, "
    f"but you can visit the official Parkside Tavern website here: {MAIN_WEBSITE_LINK}"
)

MISSING_API_KEY_MESSAGE = (
    "ParksideAI is online, but the AI connection is not configured yet. "
    f"For official Parkside Tavern information, please visit {MAIN_WEBSITE_LINK}"
)


# ============================================================
# 2. OPENAI CLIENT FACTORY
# ============================================================

def get_openai_client() -> Optional[OpenAI]:
    """
    Create the OpenAI client only when needed.

    Why:
    - Prevents Flask from crashing during startup if OPENAI_API_KEY is missing.
    - Allows Render health checks and static pages to work even if AI config is incomplete.
    - Makes local development safer.
    """

    if not settings.OPENAI_API_KEY:
        return None

    try:
        return OpenAI(api_key=settings.OPENAI_API_KEY)

    except Exception as error:
        print("OPENAI CLIENT INIT ERROR:", error)
        return None


# ============================================================
# 3. RESTAURANT KNOWLEDGE LOADER
# ============================================================

def load_restaurant_knowledge() -> str:
    """
    Load official Parkside Tavern knowledge from data/parkside_knowledge.json.

    This file should be built from:
    - https://parksidenj.com/
    - official Parkside Tavern menu pages
    - official OpenTable reservation link
    - official Tripleseat private event link
    """

    knowledge_path = Path(settings.KNOWLEDGE_FILE)

    if not knowledge_path.exists():
        print(f"KNOWLEDGE FILE MISSING: {knowledge_path}")
        return ""

    try:
        with open(knowledge_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return json.dumps(data, indent=2)

    except json.JSONDecodeError as error:
        print("KNOWLEDGE JSON ERROR:", error)
        return ""

    except Exception as error:
        print("KNOWLEDGE LOAD ERROR:", error)
        return ""


# ============================================================
# 4. PLATFORM SAFETY INSTRUCTION
# ============================================================

def build_platform_safety_instruction() -> str:
    """
    Hard safety instruction injected into every chat request.
    """

    return f"""
Critical ParksideAI platform rules:

1. ParksideAI does not take reservations directly.
2. ParksideAI does not collect guest personal information.
3. ParksideAI does not store guest personal information.
4. ParksideAI does not ask for names, phone numbers, emails, payment information, or private booking details.
5. ParksideAI does not promise availability, pricing, policies, or event package details unless they are provided in official knowledge.
6. ParksideAI should route users to official Parkside Tavern links.

Official links:
- Main Parkside Tavern website: {MAIN_WEBSITE_LINK}
- Reservations through OpenTable: {RESERVATION_LINK}
- Private events through Tripleseat: {PRIVATE_EVENTS_LINK}

Required routing:
- If the guest wants a reservation, direct them to OpenTable: {RESERVATION_LINK}
- If the guest wants a private event, party, birthday, corporate event, holiday event, or large group inquiry, direct them to Tripleseat: {PRIVATE_EVENTS_LINK}
- If the guest wants menus, hours, drinks, brunch, location, or general restaurant information, direct them to the official website: {MAIN_WEBSITE_LINK}

Never say:
- "I can book that for you."
- "What is your phone number?"
- "What is your email?"
- "Give me your contact information."
- "I will save your information."
- "I can take your reservation."

Say instead:
- "For reservations, please use Parkside Tavern’s OpenTable link."
- "For private events, please use the official private event inquiry form."
- "For current restaurant details, please visit the official Parkside Tavern website."
"""


# ============================================================
# 5. CONTEXT BUILDER
# ============================================================

def build_full_restaurant_context(
    restaurant_context: str,
    intent_analysis: Dict[str, object],
    routing_instruction: str
) -> str:
    """
    Combine official knowledge, intent analysis, routing rules,
    and privacy boundaries into one context block.
    """

    return f"""
Official Parkside Tavern Knowledge:
{restaurant_context}

Detected Guest Intent:
{json.dumps(intent_analysis, indent=2)}

Guest Intent Routing Instruction:
{routing_instruction}

Platform Safety Instruction:
{build_platform_safety_instruction()}
"""


# ============================================================
# 6. CONVERSATION HISTORY SANITIZER
# ============================================================

def sanitize_conversation_history(
    conversation_history: Optional[List[Dict[str, str]]]
) -> List[Dict[str, str]]:
    """
    Keep only valid OpenAI-style conversation messages.

    This prevents frontend mistakes from breaking the API call.
    """

    if not isinstance(conversation_history, list):
        return []

    cleaned_history = []

    for message in conversation_history:
        if not isinstance(message, dict):
            continue

        role = message.get("role")
        content = message.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not isinstance(content, str) or not content.strip():
            continue

        cleaned_history.append({
            "role": role,
            "content": content.strip()
        })

    return cleaned_history[-10:]


# ============================================================
# 7. RESPONSE POST-PROCESSING
# ============================================================

def enforce_official_routing_language(
    response_text: str,
    intent_analysis: Dict[str, object]
) -> str:
    """
    Lightweight final safety pass.

    Ensures route-specific responses include the correct official link.
    """

    if not response_text:
        return SAFE_FALLBACK_MESSAGE

    intent = intent_analysis.get("intent", "general")

    if intent == "reservation" and RESERVATION_LINK not in response_text:
        response_text += (
            f"\n\nFor reservations, please use Parkside Tavern’s OpenTable link: "
            f"{RESERVATION_LINK}"
        )

    elif intent == "private_event" and PRIVATE_EVENTS_LINK not in response_text:
        response_text += (
            f"\n\nFor private events and group inquiries, please use the official "
            f"Parkside Tavern private event form: {PRIVATE_EVENTS_LINK}"
        )

    elif intent in ["menu", "drinks", "hours", "location"] and MAIN_WEBSITE_LINK not in response_text:
        response_text += (
            f"\n\nFor the most current Parkside Tavern information, please visit: "
            f"{MAIN_WEBSITE_LINK}"
        )

    return response_text


# ============================================================
# 8. MAIN CHAT RESPONSE FUNCTION
# ============================================================

def generate_chat_response(
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Generate a guest-facing ParksideAI response.

    This function is safe:
    - It will not crash app startup.
    - It will not collect personal info.
    - It injects official routing rules.
    - It returns a useful fallback if OpenAI fails.
    """

    if not user_message or not user_message.strip():
        return "Please send me a message so I can help."

    client = get_openai_client()

    if client is None:
        return MISSING_API_KEY_MESSAGE

    clean_history = sanitize_conversation_history(conversation_history)

    restaurant_context = load_restaurant_knowledge()
    intent_analysis = analyze_guest_intent(user_message)
    routing_instruction = build_routing_instruction(intent_analysis)

    full_context = build_full_restaurant_context(
        restaurant_context=restaurant_context,
        intent_analysis=intent_analysis,
        routing_instruction=routing_instruction
    )

    messages = build_messages(
        user_message=user_message.strip(),
        restaurant_context=full_context,
        conversation_history=clean_history
    )

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
        )

        raw_reply = response.choices[0].message.content

        return enforce_official_routing_language(
            response_text=raw_reply,
            intent_analysis=intent_analysis
        )

    except Exception as error:
        print("OPENAI SERVICE ERROR:", error)
        return SAFE_FALLBACK_MESSAGE


# ============================================================
# 9. DIAGNOSTICS
# ============================================================

def get_openai_service_status() -> Dict[str, object]:
    """
    Return non-secret diagnostic information for health checks.
    """

    knowledge_path = Path(settings.KNOWLEDGE_FILE)

    return {
        "service": "openai_service",
        "configured": bool(settings.OPENAI_API_KEY),
        "model": settings.OPENAI_MODEL,
        "knowledge_file_exists": knowledge_path.exists(),
        "privacy_mode": "no_guest_info_collection",
        "official_links": {
            "main_website": MAIN_WEBSITE_LINK,
            "reservations": RESERVATION_LINK,
            "private_events": PRIVATE_EVENTS_LINK,
        }
    }