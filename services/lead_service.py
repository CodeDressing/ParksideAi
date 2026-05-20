"""
ParksideAI Guest Intent Router
Phase 3 Upgrade

IMPORTANT:
This file does NOT capture leads.
This file does NOT save guest information.
This file does NOT take reservations.

Its job is to understand why a guest is chatting and route them
to the correct official Parkside Tavern destination.

Official routing:
- General restaurant information -> https://parksidenj.com/
- Reservations -> https://www.opentable.com/r/parkside-tavern-morristown
- Private events -> https://parksidetavern.tripleseat.com/party_request/45075
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


# ============================================================
# 1. OFFICIAL LINKS
# ============================================================

OFFICIAL_LINKS = {
    "main_website": "https://parksidenj.com/",
    "reservations": "https://www.opentable.com/r/parkside-tavern-morristown",
    "private_events": "https://parksidetavern.tripleseat.com/party_request/45075",
}


# ============================================================
# 2. PRIVACY MODE
# ============================================================

PRIVACY_MODE = {
    "collects_guest_information": False,
    "stores_guest_information": False,
    "takes_reservations": False,
    "takes_payments": False,
    "routes_to_official_links": True,
}


# ============================================================
# 3. INTENT KEYWORDS
# ============================================================

INTENT_KEYWORDS = {
    "reservation": [
        "reservation",
        "reservations",
        "reserve",
        "book a table",
        "book table",
        "table for",
        "table tonight",
        "opentable",
        "dinner reservation",
        "brunch reservation",
        "make a reservation",
        "can i book",
        "can we book",
        "do you have availability",
        "available tonight",
        "available tomorrow",
        "walk in",
        "walk-ins",
        "walkins",
        "party of",
        "seating",
        "sit down",
    ],
    "private_event": [
        "private event",
        "private events",
        "event",
        "events",
        "party",
        "birthday",
        "birthday party",
        "corporate",
        "corporate event",
        "company party",
        "holiday party",
        "large group",
        "group dinner",
        "baby shower",
        "bridal shower",
        "graduation",
        "fundraiser",
        "rehearsal dinner",
        "retirement party",
        "networking event",
        "event space",
        "private room",
        "semi-private",
        "buyout",
        "catering",
        "celebration",
        "host an event",
        "book an event",
        "plan an event",
    ],
    "menu": [
        "menu",
        "food",
        "eat",
        "dinner",
        "lunch",
        "brunch",
        "kids menu",
        "dessert",
        "appetizers",
        "burger",
        "steak",
        "seafood",
        "salad",
        "gluten free",
        "gluten-free",
        "vegetarian",
        "vegan",
        "allergy",
        "allergies",
    ],
    "drinks": [
        "drinks",
        "drink menu",
        "cocktails",
        "cocktail",
        "beer",
        "wine",
        "happy hour",
        "bar",
        "mocktail",
        "mocktails",
        "draft beer",
        "beer on tap",
        "margarita",
        "espresso martini",
    ],
    "location": [
        "where are you",
        "location",
        "address",
        "directions",
        "parking",
        "park",
        "headquarters plaza",
        "morristown",
        "nearby",
        "near me",
    ],
    "hours": [
        "hours",
        "open",
        "close",
        "closing",
        "opening",
        "what time",
        "kitchen close",
        "bar close",
        "open today",
        "open tomorrow",
        "holiday hours",
    ],
    "sports": [
        "sports",
        "game",
        "football",
        "baseball",
        "basketball",
        "hockey",
        "soccer",
        "ufc",
        "boxing",
        "tv",
        "tvs",
        "watch",
    ],
    "service_help": [
        "manager",
        "complaint",
        "issue",
        "problem",
        "charged",
        "receipt",
        "lost",
        "left something",
        "call me",
        "contact",
        "speak to someone",
    ],
    "general": [
        "website",
        "park side",
        "parkside",
        "parkside tavern",
        "info",
        "information",
        "help",
    ],
}


# ============================================================
# 4. INTENT PRIORITY
# ============================================================

INTENT_PRIORITY = [
    "reservation",
    "private_event",
    "service_help",
    "menu",
    "drinks",
    "hours",
    "location",
    "sports",
    "general",
]


# ============================================================
# 5. INTENT ROUTING CONFIG
# ============================================================

INTENT_ROUTING = {
    "reservation": {
        "recommended_action": "send_to_opentable",
        "official_link": OFFICIAL_LINKS["reservations"],
        "priority": "high",
        "guest_facing_label": "Reservation",
    },
    "private_event": {
        "recommended_action": "send_to_tripleseat",
        "official_link": OFFICIAL_LINKS["private_events"],
        "priority": "high",
        "guest_facing_label": "Private Event",
    },
    "menu": {
        "recommended_action": "send_to_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "medium",
        "guest_facing_label": "Menu",
    },
    "drinks": {
        "recommended_action": "send_to_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "medium",
        "guest_facing_label": "Drinks",
    },
    "hours": {
        "recommended_action": "send_to_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "medium",
        "guest_facing_label": "Hours",
    },
    "location": {
        "recommended_action": "send_to_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "medium",
        "guest_facing_label": "Location",
    },
    "sports": {
        "recommended_action": "answer_and_offer_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "normal",
        "guest_facing_label": "Sports Viewing",
    },
    "service_help": {
        "recommended_action": "send_to_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "high",
        "guest_facing_label": "Guest Support",
    },
    "general": {
        "recommended_action": "answer_and_offer_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "normal",
        "guest_facing_label": "General Information",
    },
}


# ============================================================
# 6. DATA MODEL
# ============================================================

@dataclass
class IntentAnalysis:
    intent: str
    matched_keywords: List[str]
    recommended_action: str
    official_link: str
    priority: str
    guest_facing_label: str
    privacy_mode: Dict[str, bool]
    should_collect_guest_info: bool
    should_store_guest_info: bool
    should_take_reservation: bool


# ============================================================
# 7. TEXT NORMALIZATION
# ============================================================

def normalize_message(user_message: str) -> str:
    if not user_message:
        return ""

    return user_message.lower().strip()


# ============================================================
# 8. KEYWORD MATCHING
# ============================================================

def find_keyword_matches(message: str, keywords: List[str]) -> List[str]:
    matches = []

    for keyword in keywords:
        if keyword in message:
            matches.append(keyword)

    return matches


def score_intents(message: str) -> Dict[str, Dict[str, object]]:
    scored_results = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        matched_keywords = find_keyword_matches(message, keywords)

        if matched_keywords:
            scored_results[intent] = {
                "score": len(matched_keywords),
                "matched_keywords": matched_keywords,
            }

    return scored_results


def choose_primary_intent(scored_results: Dict[str, Dict[str, object]]) -> str:
    if not scored_results:
        return "general"

    for intent in INTENT_PRIORITY:
        if intent in scored_results:
            return intent

    return "general"


# ============================================================
# 9. MAIN INTENT ANALYZER
# ============================================================

def analyze_guest_intent(user_message: str) -> Dict[str, object]:
    """
    Analyze guest intent without collecting personal information.

    Returns a dictionary used by:
    - routes/chat_routes.py
    - services/openai_service.py
    - frontend metadata
    - future analytics
    """

    message = normalize_message(user_message)
    scored_results = score_intents(message)
    primary_intent = choose_primary_intent(scored_results)

    routing = INTENT_ROUTING.get(
        primary_intent,
        INTENT_ROUTING["general"]
    )

    matched_keywords = scored_results.get(
        primary_intent,
        {"matched_keywords": []}
    ).get("matched_keywords", [])

    analysis = IntentAnalysis(
        intent=primary_intent,
        matched_keywords=matched_keywords,
        recommended_action=routing["recommended_action"],
        official_link=routing["official_link"],
        priority=routing["priority"],
        guest_facing_label=routing["guest_facing_label"],
        privacy_mode=PRIVACY_MODE,
        should_collect_guest_info=False,
        should_store_guest_info=False,
        should_take_reservation=False,
    )

    return asdict(analysis)


# ============================================================
# 10. ROUTING INSTRUCTION BUILDER
# ============================================================

def build_routing_instruction(intent_analysis: Dict[str, object]) -> str:
    intent = intent_analysis.get("intent", "general")
    link = intent_analysis.get("official_link", OFFICIAL_LINKS["main_website"])

    if intent == "reservation":
        return (
            "The guest appears to want a reservation. "
            "Do not take the reservation directly. "
            "Do not ask for the guest's name, phone number, email, party size, date, or time. "
            f"Politely direct them to the official OpenTable reservation link: {link}"
        )

    if intent == "private_event":
        return (
            "The guest appears to be interested in a private event, party, large group, "
            "birthday, corporate event, holiday party, fundraiser, or similar event. "
            "Do not collect guest contact information. "
            "Do not ask for name, phone number, email, date, guest count, budget, or private details. "
            f"Politely direct them to the official Parkside Tavern private events inquiry form: {link}"
        )

    if intent in ["menu", "drinks", "hours", "location", "sports"]:
        return (
            "The guest is asking for restaurant information. "
            "Answer using official Parkside Tavern knowledge when available. "
            "Do not invent details. "
            f"When helpful, direct them to the official Parkside Tavern website: {link}"
        )

    if intent == "service_help":
        return (
            "The guest may need help from the restaurant team. "
            "Do not collect personal information or private details. "
            f"Politely guide them to the official Parkside Tavern website for direct restaurant contact: {link}"
        )

    return (
        "Answer helpfully using official Parkside Tavern knowledge. "
        "Do not collect guest personal information. "
        "Do not take reservations directly. "
        f"When useful, guide the guest to the official website: {link}"
    )


# ============================================================
# 11. FRONTEND QUICK ACTIONS
# ============================================================

def get_quick_action_for_intent(intent_analysis: Dict[str, object]) -> Dict[str, str]:
    intent = intent_analysis.get("intent", "general")
    link = intent_analysis.get("official_link", OFFICIAL_LINKS["main_website"])

    if intent == "reservation":
        return {
            "label": "Book on OpenTable",
            "url": link,
            "type": "external_link",
        }

    if intent == "private_event":
        return {
            "label": "Private Event Inquiry",
            "url": link,
            "type": "external_link",
        }

    return {
        "label": "Visit Parkside Tavern Website",
        "url": link,
        "type": "external_link",
    }


# ============================================================
# 12. BACKWARD-COMPATIBILITY ALIASES
# ============================================================
#
# These prevent old imports from crashing while we finish Phase 3.
# They do NOT collect or save guest information.
# ============================================================

def analyze_lead_intent(user_message: str) -> Dict[str, object]:
    return analyze_guest_intent(user_message)


def process_lead(user_message: str, *args, **kwargs) -> Dict[str, object]:
    return analyze_guest_intent(user_message)


def save_lead(*args, **kwargs) -> None:
    return None