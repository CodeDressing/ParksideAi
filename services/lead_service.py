from config.settings import settings


OFFICIAL_LINKS = {
    "main_website": "https://parksidenj.com/",
    "reservations": "https://www.opentable.com/r/parkside-tavern-morristown",
    "private_events": "https://parksidetavern.tripleseat.com/party_request/45075"
}


def analyze_guest_intent(user_message):
    message = user_message.lower()

    reservation_keywords = [
        "reservation",
        "reserve",
        "book a table",
        "table for",
        "opentable",
        "dinner reservation",
        "brunch reservation"
    ]

    private_event_keywords = [
        "private event",
        "party",
        "birthday",
        "corporate",
        "holiday party",
        "large group",
        "baby shower",
        "bridal shower",
        "graduation",
        "fundraiser",
        "rehearsal dinner",
        "event space",
        "private room"
    ]

    menu_keywords = [
        "menu",
        "food",
        "drinks",
        "cocktails",
        "brunch",
        "happy hour",
        "beer",
        "wine",
        "dinner",
        "lunch"
    ]

    matched_keywords = []

    if any(keyword in message for keyword in reservation_keywords):
        matched_keywords = [
            keyword for keyword in reservation_keywords if keyword in message
        ]

        return {
            "intent": "reservation",
            "matched_keywords": matched_keywords,
            "recommended_action": "send_to_opentable",
            "official_link": OFFICIAL_LINKS["reservations"],
            "priority": "high"
        }

    if any(keyword in message for keyword in private_event_keywords):
        matched_keywords = [
            keyword for keyword in private_event_keywords if keyword in message
        ]

        return {
            "intent": "private_event",
            "matched_keywords": matched_keywords,
            "recommended_action": "send_to_tripleseat",
            "official_link": OFFICIAL_LINKS["private_events"],
            "priority": "high"
        }

    if any(keyword in message for keyword in menu_keywords):
        matched_keywords = [
            keyword for keyword in menu_keywords if keyword in message
        ]

        return {
            "intent": "restaurant_info",
            "matched_keywords": matched_keywords,
            "recommended_action": "send_to_official_website",
            "official_link": OFFICIAL_LINKS["main_website"],
            "priority": "medium"
        }

    return {
        "intent": "general",
        "matched_keywords": [],
        "recommended_action": "answer_and_offer_official_website",
        "official_link": OFFICIAL_LINKS["main_website"],
        "priority": "normal"
    }


def build_routing_instruction(intent_analysis):
    intent = intent_analysis.get("intent")
    link = intent_analysis.get("official_link")

    if intent == "reservation":
        return (
            "For reservations, direct the guest to OpenTable. "
            f"Official reservation link: {link}. "
            "Do not collect reservation details directly."
        )

    if intent == "private_event":
        return (
            "For private events, parties, and large group inquiries, direct the guest "
            f"to the official Tripleseat inquiry form: {link}. "
            "Do not collect guest contact information directly."
        )

    if intent == "restaurant_info":
        return (
            "For menus, hours, drinks, brunch, happy hour, and restaurant details, "
            f"direct the guest to the official Parkside Tavern website: {link}."
        )

    return (
        "Answer helpfully using official Parkside Tavern knowledge. "
        f"When useful, guide the guest to the official website: {link}."
    )