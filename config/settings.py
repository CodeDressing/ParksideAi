import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ============================================================
    # 1. APP IDENTITY
    # ============================================================

    APP_NAME = os.getenv("APP_NAME", "ParksideAI")
    RESTAURANT_NAME = os.getenv("RESTAURANT_NAME", "Parkside Tavern")
    RESTAURANT_LEGAL_BRAND = os.getenv("RESTAURANT_LEGAL_BRAND", "Parkside Tavern")

    # ============================================================
    # 2. OFFICIAL LINKS
    # ============================================================

    OFFICIAL_MAIN_WEBSITE = os.getenv(
        "OFFICIAL_MAIN_WEBSITE",
        "https://parksidenj.com/"
    )

    OFFICIAL_RESERVATION_LINK = os.getenv(
        "OFFICIAL_RESERVATION_LINK",
        "https://www.opentable.com/r/parkside-tavern-morristown"
    )

    OFFICIAL_PRIVATE_EVENTS_LINK = os.getenv(
        "OFFICIAL_PRIVATE_EVENTS_LINK",
        "https://parksidetavern.tripleseat.com/party_request/45075"
    )

    OFFICIAL_FOOD_MENU_LINK = os.getenv(
        "OFFICIAL_FOOD_MENU_LINK",
        "https://parksidenj.com/morristown-morristown-parkside-tavern-food-menu"
    )

    OFFICIAL_DRINK_MENU_LINK = os.getenv(
        "OFFICIAL_DRINK_MENU_LINK",
        "https://parksidenj.com/morristown-morristown-parkside-tavern-drink-menu"
    )

    # ============================================================
    # 3. PRIVACY / PLATFORM BOUNDARIES
    # ============================================================

    TAKES_RESERVATIONS = False
    COLLECTS_GUEST_INFO = False
    STORES_GUEST_INFO = False
    TAKES_PAYMENTS = False

    PRIVACY_MODE = "official_link_routing_only"

    PLATFORM_RULES = [
        "ParksideAI does not take reservations directly.",
        "ParksideAI does not collect guest personal information.",
        "ParksideAI does not store guest personal information.",
        "ParksideAI does not take payments.",
        "ParksideAI routes reservations to OpenTable.",
        "ParksideAI routes private events to Tripleseat.",
        "ParksideAI routes restaurant information to the official Parkside Tavern website."
    ]

    # ============================================================
    # 4. OPENAI CONFIGURATION
    # ============================================================

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.65"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "750"))

    # ============================================================
    # 5. FLASK / SERVER CONFIGURATION
    # ============================================================

    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "parkside-production-key-change-this")

    # ============================================================
    # 6. FILE PATHS
    # ============================================================

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DATA_DIR = os.getenv(
        "DATA_DIR",
        os.path.join(BASE_DIR, "data")
    )

    SEO_DATA_DIR = os.getenv(
        "SEO_DATA_DIR",
        os.path.join(BASE_DIR, "seo_pages")
    )

    KNOWLEDGE_FILE = os.getenv(
        "KNOWLEDGE_FILE",
        os.path.join(DATA_DIR, "parkside_knowledge.json")
    )

    SEO_PAGES_FILE = os.getenv(
        "SEO_PAGES_FILE",
        os.path.join(DATA_DIR, "seo_pages.json")
    )

    # ============================================================
    # 7. LOCAL SEO IDENTITY
    # ============================================================

    RESTAURANT_CITY = "Morristown"
    RESTAURANT_STATE = "NJ"
    RESTAURANT_REGION = "Morris County"
    RESTAURANT_ADDRESS = "9 Speedwell Ave, Morristown, NJ 07960"
    RESTAURANT_NEIGHBORHOOD = "Headquarters Plaza"

    LOCAL_SEO_IDENTITY = {
        "city": RESTAURANT_CITY,
        "state": RESTAURANT_STATE,
        "region": RESTAURANT_REGION,
        "address": RESTAURANT_ADDRESS,
        "neighborhood": RESTAURANT_NEIGHBORHOOD
    }

    # ============================================================
    # 8. PRIMARY SEO KEYWORDS
    # ============================================================

    SEO_PRIMARY_KEYWORDS = [
        "Parkside Tavern",
        "Parkside Tavern Morristown",
        "Morristown restaurant",
        "Morristown tavern",
        "Morristown cocktail bar",
        "restaurant in Morristown NJ",
        "tavern in Morristown NJ",
        "cocktail bar in Morristown NJ",
        "restaurant near Headquarters Plaza",
        "bar near Headquarters Plaza",
        "brunch in Morristown",
        "happy hour in Morristown",
        "dinner in Morristown",
        "drinks in Morristown",
        "private events in Morristown",
        "birthday party restaurant Morristown",
        "corporate event venue Morristown",
        "holiday party venue Morristown",
        "sports bar Morristown",
        "group dining Morristown"
    ]

    # ============================================================
    # 9. SEO SERVICE CATEGORIES
    # ============================================================

    SEO_SERVICE_CATEGORIES = {
        "private-events": {
            "title": "Private Events",
            "primary_keyword": "private events in Morristown",
            "intent": "private_event",
            "official_link": OFFICIAL_PRIVATE_EVENTS_LINK,
            "routing_action": "send_to_tripleseat"
        },
        "birthday-parties": {
            "title": "Birthday Parties",
            "primary_keyword": "birthday party restaurant Morristown",
            "intent": "private_event",
            "official_link": OFFICIAL_PRIVATE_EVENTS_LINK,
            "routing_action": "send_to_tripleseat"
        },
        "corporate-events": {
            "title": "Corporate Events",
            "primary_keyword": "corporate event venue Morristown",
            "intent": "private_event",
            "official_link": OFFICIAL_PRIVATE_EVENTS_LINK,
            "routing_action": "send_to_tripleseat"
        },
        "holiday-parties": {
            "title": "Holiday Parties",
            "primary_keyword": "holiday party venue Morristown",
            "intent": "private_event",
            "official_link": OFFICIAL_PRIVATE_EVENTS_LINK,
            "routing_action": "send_to_tripleseat"
        },
        "lunch":
            (
                f"{self.restaurant_name} offers lunch in "
                f"{self.city} for professionals, visitors, "
                f"and guests looking for food, cocktails, "
                f"and hospitality near Headquarters Plaza."
            )
        "brunch": {
            "title": "Brunch",
            "primary_keyword": "brunch in Morristown",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_MAIN_WEBSITE,
            "routing_action": "send_to_official_website"
        },
        "happy-hour": {
            "title": "Happy Hour",
            "primary_keyword": "happy hour in Morristown",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_MAIN_WEBSITE,
            "routing_action": "send_to_official_website"
        },
        "cocktails": {
            "title": "Cocktails",
            "primary_keyword": "cocktail bar in Morristown NJ",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_DRINK_MENU_LINK,
            "routing_action": "send_to_official_website"
        },
        "dinner": {
            "title": "Dinner",
            "primary_keyword": "dinner in Morristown",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_FOOD_MENU_LINK,
            "routing_action": "send_to_official_website"
        },
        "sports-viewing": {
            "title": "Sports Viewing",
            "primary_keyword": "sports bar Morristown",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_MAIN_WEBSITE,
            "routing_action": "send_to_official_website"
        },
        "group-dining": {
            "title": "Group Dining",
            "primary_keyword": "group dining Morristown",
            "intent": "private_event",
            "official_link": OFFICIAL_PRIVATE_EVENTS_LINK,
            "routing_action": "send_to_tripleseat"
        }
        ,

        "sports-bar-morristown": {
            "title": "Sports Bar Morristown NJ",
            "primary_keyword": "sports bar Morristown NJ",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_MAIN_WEBSITE,
            "routing_action": "send_to_official_website"
        },

        "craft-cocktails-morristown": {
            "title": "Craft Cocktails Morristown NJ",
            "primary_keyword": "craft cocktails Morristown NJ",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_DRINK_MENU_LINK,
            "routing_action": "send_to_official_website"
        },

        "nightlife-morristown": {
            "title": "Nightlife Morristown NJ",
            "primary_keyword": "nightlife Morristown NJ",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_MAIN_WEBSITE,
            "routing_action": "send_to_official_website"
        },

        "weekend-brunch-morristown": {
            "title": "Weekend Brunch Morristown NJ",
            "primary_keyword": "weekend brunch Morristown NJ",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_FOOD_MENU_LINK,
            "routing_action": "send_to_official_website"
        },

        "bars-near-headquarters-plaza": {
            "title": "Bars Near Headquarters Plaza",
            "primary_keyword": "bars near Headquarters Plaza Morristown",
            "intent": "restaurant_info",
            "official_link": OFFICIAL_MAIN_WEBSITE,
            "routing_action": "send_to_official_website"
        }
    }

    # ============================================================
    # 10. LOCATION TARGETS
    # ============================================================

    SEO_LOCATION_TARGETS = [
        "Morristown",
        "Morris County",
        "Headquarters Plaza",
        "Morris Plains",
        "Madison",
        "Chatham",
        "Mendham",
        "Randolph",
        "Denville",
        "Parsippany",
        "Florham Park",
        "Cedar Knolls",
        "Convent Station"
    ]

    # ============================================================
    # 11. SEO PAGE RULES
    # ============================================================

    SEO_PAGE_RULES = [
        "Use official Parkside Tavern information first.",
        "Do not invent offers, specials, prices, hours, or availability.",
        "Do not claim reservations can be made through ParksideAI.",
        "Do not collect guest contact information.",
        "For reservations, route users to OpenTable.",
        "For private events, route users to Tripleseat.",
        "For menu, drinks, hours, and general restaurant information, route users to parksidenj.com.",
        "Use natural local SEO language.",
        "Do not keyword-stuff.",
        "Make every page useful to guests."
    ]

    # ============================================================
    # 12. SEO META DEFAULTS
    # ============================================================

    SEO_DEFAULT_TITLE_SUFFIX = " | Parkside Tavern Morristown NJ"

    SEO_DEFAULT_DESCRIPTION = (
        "Explore Parkside Tavern in Morristown NJ for dining, drinks, brunch, "
        "happy hour, private events, and local hospitality. ParksideAI routes "
        "guests to official Parkside Tavern links."
    )

    SEO_DEFAULT_IMAGE_ALT = "Parkside Tavern in Morristown NJ"

    # ============================================================
    # 13. INTENT ROUTING KEYWORDS
    # ============================================================

    RESERVATION_KEYWORDS = [
        "reservation",
        "reservations",
        "reserve",
        "book a table",
        "table for",
        "opentable",
        "availability",
        "dinner reservation",
        "brunch reservation"
    ]

    PRIVATE_EVENT_KEYWORDS = [
        "private event",
        "private events",
        "party",
        "birthday",
        "birthday party",
        "corporate event",
        "holiday party",
        "large group",
        "group dining",
        "baby shower",
        "bridal shower",
        "graduation",
        "fundraiser",
        "rehearsal dinner",
        "retirement party",
        "networking event",
        "event space",
        "private room",
        "buyout",
        "catering"
    ]

    RESTAURANT_INFO_KEYWORDS = [
        "menu",
        "food",
        "drinks",
        "cocktails",
        "beer",
        "wine",
        "brunch",
        "dinner",
        "lunch",
        "happy hour",
        "hours",
        "location",
        "parking",
        "directions",
        "sports",
        "tv",
        "tvs"
    ]

    # Backward compatibility
    LEAD_KEYWORDS = PRIVATE_EVENT_KEYWORDS + RESERVATION_KEYWORDS

    # ============================================================
    # 14. SCHEMA / STRUCTURED DATA DEFAULTS
    # ============================================================

    LOCAL_BUSINESS_SCHEMA_TYPE = "Restaurant"

    STRUCTURED_DATA_DEFAULTS = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": RESTAURANT_NAME,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "9 Speedwell Ave",
            "addressLocality": "Morristown",
            "addressRegion": "NJ",
            "postalCode": "07960",
            "addressCountry": "US"
        },
        "url": OFFICIAL_MAIN_WEBSITE,
        "servesCuisine": "American",
        "priceRange": "$$"
    }


settings = Settings()