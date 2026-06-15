"""
ParksideAI Guest Intent Router
Phase 7 Part 2.0 — Hospitality Semantic Intelligence Engine

This file does NOT capture leads.
This file does NOT save guest information.
This file does NOT take reservations.

Its job is to understand guest intent, detect hospitality context,
score semantic meaning, and route guests to the correct official
Parkside Tavern destination.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import re


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
# 3. SEMANTIC INTENT VOCABULARY
# ============================================================

INTENT_KEYWORDS = {
    "reservation": [
        "reservation", "reservations", "reserve", "book a table", "book table",
        "grab a table", "get a table", "table for", "table tonight",
        "opentable", "dinner reservation", "brunch reservation",
        "make a reservation", "can i book", "can we book",
        "do you have availability", "available tonight", "available tomorrow",
        "walk in", "walk-ins", "walkins", "party of", "seating", "sit down",
        "come in tonight", "eat tonight", "dinner for two", "lunch for two",
    ],
    "private_event": [
        "private event", "private events", "event", "events", "party",
        "birthday", "birthday party", "corporate", "corporate event",
        "company party", "team dinner", "office party", "office gathering",
        "holiday party", "large group", "group dinner", "baby shower",
        "bridal shower", "graduation", "fundraiser", "rehearsal dinner",
        "retirement party", "networking event", "event space", "private room",
        "semi-private", "buyout", "catering", "celebration",
        "host an event", "book an event", "plan an event", "group of",
    ],
    "menu": [
        "menu", "food", "eat", "dinner", "lunch", "brunch", "kids menu",
        "dessert", "appetizers", "burger", "steak", "seafood", "salad",
        "gluten free", "gluten-free", "vegetarian", "vegan", "allergy",
        "allergies", "what do you serve", "food options",
    ],
    "drinks": [
        "drinks", "drink menu", "cocktails", "cocktail", "beer", "wine",
        "happy hour", "bar", "mocktail", "mocktails", "draft beer",
        "beer on tap", "margarita", "espresso martini", "after work drinks",
    ],
    "location": [
        "where are you", "location", "address", "directions", "parking",
        "park", "headquarters plaza", "morristown", "nearby", "near me",
        "how do i get there",
    ],
    "hours": [
        "hours", "open", "close", "closing", "opening", "what time",
        "kitchen close", "bar close", "open today", "open tomorrow",
        "holiday hours",
    ],
    "sports": [
        "sports", "game", "football", "baseball", "basketball", "hockey",
        "soccer", "ufc", "boxing", "tv", "tvs", "watch", "watch the game",
    ],
    "service_help": [
        "manager", "complaint", "issue", "problem", "charged", "receipt",
        "lost", "left something", "call me", "contact", "speak to someone",
    ],
    "general": [
        "website", "park side", "parkside", "parkside tavern", "info",
        "information", "help",
    ],
}


# ============================================================
# 4. HOSPITALITY ENTITY VOCABULARY
# ============================================================

ENTITY_PATTERNS = {
    "occasion": {
        "birthday": ["birthday", "bday"],
        "anniversary": ["anniversary"],
        "corporate": ["corporate", "company", "office", "team", "business"],
        "holiday_party": ["holiday party", "christmas party", "winter party"],
        "fundraiser": ["fundraiser", "charity"],
        "graduation": ["graduation", "graduate"],
        "date_night": ["date night", "romantic", "dinner date"],
        "family_meal": ["family", "kids", "parents"],
    },
    "meal_period": {
        "brunch": ["brunch"],
        "lunch": ["lunch", "midday", "afternoon"],
        "dinner": ["dinner", "tonight", "evening"],
        "happy_hour": ["happy hour", "after work"],
    },
    "beverage_interest": {
        "cocktails": ["cocktail", "cocktails", "martini", "margarita"],
        "beer": ["beer", "draft", "tap"],
        "wine": ["wine"],
        "mocktails": ["mocktail", "mocktails"],
    },
    "guest_need": {
        "reservation": ["book", "reserve", "reservation", "table"],
        "private_event": ["event", "party", "private room", "buyout"],
        "menu": ["menu", "food", "eat"],
        "support": ["manager", "receipt", "lost", "complaint"],
    },
}


# ============================================================
# 5. INTENT PRIORITY AND ROUTING
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
    confidence_score: int
    intent_scores: Dict[str, int]
    entities: Dict[str, Any]
    opportunity_type: str
    semantic_summary: str


# ============================================================
# 7. TEXT NORMALIZATION
# ============================================================

def normalize_message(user_message: str) -> str:
    if not user_message:
        return ""

    return re.sub(r"\s+", " ", user_message.lower().strip())


# ============================================================
# 8. SEMANTIC MATCHING
# ============================================================

def find_keyword_matches(message: str, keywords: List[str]) -> List[str]:
    return [keyword for keyword in keywords if keyword in message]


def score_intents(message: str) -> Dict[str, Dict[str, object]]:
    scored_results = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        matched_keywords = find_keyword_matches(message, keywords)
        score = len(matched_keywords) * 10

        if intent == "private_event" and detect_party_size(message) >= 10:
            score += 25

        if intent == "reservation" and detect_party_size(message) in range(1, 10):
            score += 15

        if intent == "drinks" and "happy hour" in message:
            score += 20

        if matched_keywords or score > 0:
            scored_results[intent] = {
                "score": score,
                "matched_keywords": matched_keywords,
            }

    return scored_results


def choose_primary_intent(scored_results: Dict[str, Dict[str, object]]) -> str:
    if not scored_results:
        return "general"

    highest_score = max(
        result["score"] for result in scored_results.values()
    )

    top_intents = [
        intent for intent, result in scored_results.items()
        if result["score"] == highest_score
    ]

    for intent in INTENT_PRIORITY:
        if intent in top_intents:
            return intent

    return "general"


# ============================================================
# 9. ENTITY EXTRACTION
# ============================================================

def detect_party_size(message: str) -> int:
    patterns = [
        r"party of (\d+)",
        r"group of (\d+)",
        r"for (\d+) people",
        r"for (\d+)",
        r"(\d+) people",
        r"(\d+) guests",
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return 0

    return 0


def extract_entities(message: str) -> Dict[str, Any]:
    entities: Dict[str, Any] = {
        "party_size": detect_party_size(message),
        "occasion": [],
        "meal_period": [],
        "beverage_interest": [],
        "guest_need": [],
    }

    for entity_type, groups in ENTITY_PATTERNS.items():
        for label, keywords in groups.items():
            if any(keyword in message for keyword in keywords):
                entities[entity_type].append(label)

    return entities


# ============================================================
# 10. CONFIDENCE AND OPPORTUNITY DETECTION
# ============================================================

def calculate_confidence(primary_intent: str, scored_results: Dict[str, Dict[str, object]]) -> int:
    if primary_intent not in scored_results:
        return 35

    score = int(scored_results[primary_intent]["score"])

    if score >= 50:
        return 95

    if score >= 30:
        return 85

    if score >= 20:
        return 75

    if score >= 10:
        return 62

    return 40


def detect_opportunity_type(primary_intent: str, entities: Dict[str, Any]) -> str:
    party_size = entities.get("party_size", 0)
    occasions = entities.get("occasion", [])
    meal_periods = entities.get("meal_period", [])

    if primary_intent == "private_event":
        if "corporate" in occasions:
            return "corporate_event"
        if "birthday" in occasions:
            return "birthday_event"
        if party_size >= 10:
            return "large_group_event"
        return "private_event_inquiry"

    if primary_intent == "reservation":
        if "date_night" in occasions:
            return "date_night_reservation"
        if "brunch" in meal_periods:
            return "brunch_reservation"
        return "standard_reservation"

    if primary_intent == "drinks":
        if "happy_hour" in meal_periods:
            return "happy_hour_discovery"
        return "drink_menu_discovery"

    if primary_intent == "menu":
        return "menu_discovery"

    return "general_guest_support"


def build_semantic_summary(primary_intent: str, entities: Dict[str, Any], confidence: int) -> str:
    return (
        f"Detected intent: {primary_intent}. "
        f"Confidence: {confidence}. "
        f"Entities: {entities}."
    )


# ============================================================
# 11. MAIN INTENT ANALYZER
# ============================================================

def analyze_guest_intent(user_message: str) -> Dict[str, object]:
    message = normalize_message(user_message)
    scored_results = score_intents(message)
    primary_intent = choose_primary_intent(scored_results)
    routing = INTENT_ROUTING.get(primary_intent, INTENT_ROUTING["general"])

    matched_keywords = scored_results.get(
        primary_intent,
        {"matched_keywords": []}
    ).get("matched_keywords", [])

    intent_scores = {
        intent: int(result["score"])
        for intent, result in scored_results.items()
    }

    entities = extract_entities(message)
    confidence_score = calculate_confidence(primary_intent, scored_results)
    opportunity_type = detect_opportunity_type(primary_intent, entities)
    semantic_summary = build_semantic_summary(
        primary_intent,
        entities,
        confidence_score
    )

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
        confidence_score=confidence_score,
        intent_scores=intent_scores,
        entities=entities,
        opportunity_type=opportunity_type,
        semantic_summary=semantic_summary,
    )

    return asdict(analysis)


# ============================================================
# 12. ROUTING INSTRUCTION BUILDER
# ============================================================

def build_routing_instruction(intent_analysis: Dict[str, object]) -> str:
    intent = intent_analysis.get("intent", "general")
    link = intent_analysis.get("official_link", OFFICIAL_LINKS["main_website"])
    opportunity_type = intent_analysis.get("opportunity_type", "general_guest_support")
    confidence_score = intent_analysis.get("confidence_score", 0)

    if intent == "reservation":
        return (
            "The guest appears to want a reservation. "
            f"Detected opportunity type: {opportunity_type}. "
            f"Confidence score: {confidence_score}. "
            "Do not take the reservation directly. "
            "Do not ask for the guest's name, phone number, email, party size, date, or time. "
            f"Politely direct them to the official OpenTable reservation link: {link}"
        )

    if intent == "private_event":
        return (
            "The guest appears to be interested in a private event, party, large group, "
            "birthday, corporate event, holiday party, fundraiser, or similar event. "
            f"Detected opportunity type: {opportunity_type}. "
            f"Confidence score: {confidence_score}. "
            "Do not collect guest contact information. "
            "Do not ask for name, phone number, email, date, guest count, budget, or private details. "
            f"Politely direct them to the official Parkside Tavern private events inquiry form: {link}"
        )

    if intent in ["menu", "drinks", "hours", "location", "sports"]:
        return (
            "The guest is asking for restaurant information. "
            f"Detected opportunity type: {opportunity_type}. "
            f"Confidence score: {confidence_score}. "
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
# 13. FRONTEND QUICK ACTIONS
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

    if intent == "drinks":
        return {
            "label": "View Drink Information",
            "url": link,
            "type": "external_link",
        }

    if intent == "menu":
        return {
            "label": "View Menu Information",
            "url": link,
            "type": "external_link",
        }

    return {
        "label": "Visit Parkside Tavern Website",
        "url": link,
        "type": "external_link",
    }


# ============================================================
# 14. BACKWARD-COMPATIBILITY ALIASES
# ============================================================

def analyze_lead_intent(user_message: str) -> Dict[str, object]:
    return analyze_guest_intent(user_message)


def process_lead(user_message: str, *args, **kwargs) -> Dict[str, object]:
    return analyze_guest_intent(user_message)


def save_lead(*args, **kwargs) -> None:
    return None