"""
============================================================
ParksideAI
Main Routes Controller
Phase 5 Part 1.0
============================================================

Responsibilities:
- Homepage rendering
- Global SEO metadata
- Trust routing
- Footer data
- Official link exposure
- Public platform presentation
- Future analytics hooks
"""

# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

from flask import Blueprint
from flask import render_template

from config.settings import settings


# ============================================================
# SECTION 2 — BLUEPRINT SETUP
# ============================================================

main_bp = Blueprint(
    "main",
    __name__
)


# ============================================================
# SECTION 3 — GLOBAL PLATFORM CONTEXT
# ============================================================

GLOBAL_PLATFORM_CONTEXT = {

    "platform_name":
        settings.APP_NAME,

    "restaurant_name":
        settings.RESTAURANT_NAME,

    "city":
        settings.RESTAURANT_CITY,

    "state":
        settings.RESTAURANT_STATE,

    "official_links": {

        "website":
            settings.OFFICIAL_MAIN_WEBSITE,

        "reservations":
            settings.OFFICIAL_RESERVATION_LINK,

        "private_events":
            settings.OFFICIAL_PRIVATE_EVENTS_LINK,

        "food_menu":
            settings.OFFICIAL_FOOD_MENU_LINK,

        "drink_menu":
            settings.OFFICIAL_DRINK_MENU_LINK
    },

    "privacy_mode":
        settings.PRIVACY_MODE
}


# ============================================================
# SECTION 4 — HOMEPAGE SEO DATA
# ============================================================

HOMEPAGE_SEO_DATA = {

    "title":
        "ParksideAI | Parkside Tavern Hospitality Assistant",

    "description":
        (
            "ParksideAI helps guests discover official "
            "Parkside Tavern information including "
            "reservations, private events, menus, "
            "cocktails, brunch, happy hour, and "
            "Morristown restaurant details."
        ),

    "keywords": [

        "Parkside Tavern",
        "ParksideAI",
        "Morristown restaurant",
        "Morristown tavern",
        "Morristown cocktails",
        "Morristown brunch",
        "private events Morristown",
        "Parkside Tavern reservations",
        "Morristown nightlife",
        "Morristown dining"
    ],

    "canonical":
        settings.OFFICIAL_MAIN_WEBSITE
}


# ============================================================
# SECTION 5 — HOMEPAGE FEATURE CARDS
# ============================================================

HOMEPAGE_FEATURE_CARDS = [

    {
        "title":
            "Reservations",

        "description":
            (
                "Use the official OpenTable page "
                "for Parkside Tavern reservations."
            ),

        "url":
            settings.OFFICIAL_RESERVATION_LINK,

        "button":
            "Book on OpenTable"
    },

    {
        "title":
            "Private Events",

        "description":
            (
                "Submit official inquiries for "
                "parties, celebrations, and "
                "group gatherings."
            ),

        "url":
            settings.OFFICIAL_PRIVATE_EVENTS_LINK,

        "button":
            "Event Inquiry"
    },

    {
        "title":
            "Food Menu",

        "description":
            (
                "Explore Parkside Tavern food "
                "offerings and dining information."
            ),

        "url":
            settings.OFFICIAL_FOOD_MENU_LINK,

        "button":
            "View Menu"
    },

    {
        "title":
            "Drink Menu",

        "description":
            (
                "Explore cocktails, spirits, wine, "
                "beer, and bar offerings."
            ),

        "url":
            settings.OFFICIAL_DRINK_MENU_LINK,

        "button":
            "View Drinks"
    }
]


# ============================================================
# SECTION 6 — SEO PAGE PREVIEW CARDS
# ============================================================

SEO_PREVIEW_CARDS = [

    {
        "title":
            "Private Events",

        "url":
            "/seo/private-events",

        "description":
            (
                "Morristown private event discovery "
                "and hospitality routing."
            )
    },

    {
        "title":
            "Birthday Parties",

        "url":
            "/seo/birthday-parties",

        "description":
            (
                "Birthday celebrations and group "
                "dining discovery."
            )
    },

    {
        "title":
            "Corporate Events",

        "url":
            "/seo/corporate-events",

        "description":
            (
                "Business dinners and corporate "
                "gathering routing."
            )
    },

    {
        "title":
            "Holiday Parties",

        "url":
            "/seo/holiday-parties",

        "description":
            (
                "Holiday hospitality and event "
                "discovery pages."
            )
    },

    {
        "title":
            "Brunch",

        "url":
            "/seo/brunch",

        "description":
            (
                "Brunch discovery for Morristown "
                "restaurant guests."
            )
    },

    {
        "title":
            "Cocktails",

        "url":
            "/seo/cocktails",

        "description":
            (
                "Cocktail bar discovery and "
                "drink menu routing."
            )
    }
]


# ============================================================
# SECTION 7 — TRUST / PRIVACY DATA
# ============================================================

TRUST_DATA = [

    {
        "title":
            "Official Reservation Routing",

        "description":
            (
                "ParksideAI routes reservation "
                "guests directly to OpenTable."
            )
    },

    {
        "title":
            "No Guest Data Collection",

        "description":
            (
                "ParksideAI does not collect "
                "names, phone numbers, emails, "
                "or payment information."
            )
    },

    {
        "title":
            "Official Information First",

        "description":
            (
                "Restaurant information is "
                "sourced from official "
                "Parkside Tavern platforms."
            )
    }
]


# ============================================================
# SECTION 8 — FOOTER DATA
# ============================================================

FOOTER_LINKS = [

    {
        "label":
            "Official Website",

        "url":
            settings.OFFICIAL_MAIN_WEBSITE
    },

    {
        "label":
            "Reservations",

        "url":
            settings.OFFICIAL_RESERVATION_LINK
    },

    {
        "label":
            "Private Events",

        "url":
            settings.OFFICIAL_PRIVATE_EVENTS_LINK
    }
]


# ============================================================
# SECTION 9 — MAIN HOMEPAGE
# ============================================================

@main_bp.route("/")
def home():
    """
    Render the ParksideAI homepage.
    """

    return render_template(

        "index.html",

        platform=GLOBAL_PLATFORM_CONTEXT,

        seo=HOMEPAGE_SEO_DATA,

        feature_cards=HOMEPAGE_FEATURE_CARDS,

        seo_cards=SEO_PREVIEW_CARDS,

        trust_cards=TRUST_DATA,

        footer_links=FOOTER_LINKS
    )


# ============================================================
# SECTION 10 — PRIVACY PAGE
# ============================================================

@main_bp.route("/privacy")
def privacy():
    """
    Privacy policy route.
    """

    return render_template(

        "privacy.html",

        platform=GLOBAL_PLATFORM_CONTEXT
    )


# ============================================================
# SECTION 11 — TERMS PAGE
# ============================================================

@main_bp.route("/terms")
def terms():
    """
    Terms of service route.
    """

    return render_template(

        "terms.html",

        platform=GLOBAL_PLATFORM_CONTEXT
    )


# ============================================================
# SECTION 12 — HEALTH CHECK
# ============================================================

@main_bp.route("/health")
def health():
    """
    Lightweight Render health check.
    """

    return {

        "success": True,

        "platform":
            settings.APP_NAME,

        "restaurant":
            settings.RESTAURANT_NAME,

        "status":
            "online",

        "privacy_mode":
            settings.PRIVACY_MODE
    }