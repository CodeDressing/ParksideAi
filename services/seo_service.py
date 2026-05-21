"""
ParksideAI SEO Service
Phase 4 Upgrade

Responsibilities:
- Build SEO metadata
- Generate local SEO page data
- Support dynamic SEO landing pages
- Provide structured data
- Keep all booking/event actions routed to official links
- Never collect guest information
"""

from typing import Any, Dict, List, Optional

from config.settings import settings


class SEOService:
    def __init__(self):
        self.restaurant_name = settings.RESTAURANT_NAME
        self.city = settings.RESTAURANT_CITY
        self.state = settings.RESTAURANT_STATE
        self.region = settings.RESTAURANT_REGION
        self.address = settings.RESTAURANT_ADDRESS

        self.main_website = settings.OFFICIAL_MAIN_WEBSITE
        self.reservation_link = settings.OFFICIAL_RESERVATION_LINK
        self.private_events_link = settings.OFFICIAL_PRIVATE_EVENTS_LINK
        self.food_menu_link = settings.OFFICIAL_FOOD_MENU_LINK
        self.drink_menu_link = settings.OFFICIAL_DRINK_MENU_LINK

    # ============================================================
    # 1. INTENT DETECTION
    # ============================================================

    def detect_seo_intent(self, query: str) -> str:
        query_lower = (query or "").lower()

        if any(keyword in query_lower for keyword in settings.RESERVATION_KEYWORDS):
            return "reservation"

        if any(keyword in query_lower for keyword in settings.PRIVATE_EVENT_KEYWORDS):
            return "private_event"

        if any(keyword in query_lower for keyword in settings.RESTAURANT_INFO_KEYWORDS):
            return "restaurant_info"

        return "general"

    # ============================================================
    # 2. KEYWORD CONTEXT
    # ============================================================

    def generate_keyword_context(self, user_query: str = "") -> Dict[str, Any]:
        return {
            "restaurant": self.restaurant_name,
            "location": {
                "city": self.city,
                "state": self.state,
                "region": self.region,
                "address": self.address,
                "neighborhood": settings.RESTAURANT_NEIGHBORHOOD
            },
            "primary_keywords": settings.SEO_PRIMARY_KEYWORDS,
            "location_targets": settings.SEO_LOCATION_TARGETS,
            "semantic_topics": self.get_semantic_topics(),
            "query_intent": self.detect_seo_intent(user_query),
            "official_links": self.get_official_links(),
            "privacy_mode": settings.PRIVACY_MODE
        }

    def get_semantic_topics(self) -> List[str]:
        return [
            "Morristown dining",
            "cocktail destination",
            "local tavern",
            "group dining",
            "private event venue",
            "social dining experience",
            "sports viewing",
            "brunch destination",
            "happy hour destination",
            "nightlife in Morristown",
            "restaurant near Headquarters Plaza",
            "Morris County restaurant",
            "Morristown cocktail bar",
            "Morristown private events",
            "Morristown group dining"
        ]

    # ============================================================
    # 3. OFFICIAL LINKS
    # ============================================================

    def get_official_links(self) -> Dict[str, str]:
        return {
            "main_website": self.main_website,
            "reservations": self.reservation_link,
            "private_events": self.private_events_link,
            "food_menu": self.food_menu_link,
            "drink_menu": self.drink_menu_link
        }

    def get_cta_for_intent(self, intent: str) -> Dict[str, str]:
        if intent == "reservation":
            return {
                "label": "Book on OpenTable",
                "url": self.reservation_link,
                "type": "official_reservation_link"
            }

        if intent == "private_event":
            return {
                "label": "Submit Private Event Inquiry",
                "url": self.private_events_link,
                "type": "official_private_event_link"
            }

        if intent == "drinks":
            return {
                "label": "View Drink Menu",
                "url": self.drink_menu_link,
                "type": "official_menu_link"
            }

        if intent == "food":
            return {
                "label": "View Food Menu",
                "url": self.food_menu_link,
                "type": "official_menu_link"
            }

        return {
            "label": "Visit Official Website",
            "url": self.main_website,
            "type": "official_website_link"
        }

    # ============================================================
    # 4. SEO PAGE CONFIG
    # ============================================================

    def get_page_config(self, slug: str) -> Optional[Dict[str, Any]]:
        return settings.SEO_SERVICE_CATEGORIES.get(slug)

    def list_available_pages(self) -> List[Dict[str, Any]]:
        pages = []

        for slug, config in settings.SEO_SERVICE_CATEGORIES.items():
            pages.append({
                "slug": slug,
                "title": config["title"],
                "primary_keyword": config["primary_keyword"],
                "intent": config["intent"],
                "url_path": f"/seo/{slug}",
                "official_link": config["official_link"]
            })

        return pages

    # ============================================================
    # 5. META TAG GENERATION
    # ============================================================

    def build_meta_tags(self, page_type: str = "general") -> Dict[str, str]:
        config = self.get_page_config(page_type)

        if config:
            title = f"{config['title']} in {self.city} NJ{settings.SEO_DEFAULT_TITLE_SUFFIX}"
            description = (
                f"Explore {config['primary_keyword']} with {self.restaurant_name}. "
                f"Find official Parkside Tavern information and use the correct official link "
                f"for reservations, private events, menus, and restaurant details."
            )

            return {
                "title": title,
                "description": description[:300],
                "canonical": f"{self.main_website}",
                "robots": "index, follow",
                "primary_keyword": config["primary_keyword"]
            }

        return {
            "title": f"{self.restaurant_name} | {self.city} NJ Restaurant, Tavern & Cocktail Bar",
            "description": settings.SEO_DEFAULT_DESCRIPTION,
            "canonical": self.main_website,
            "robots": "index, follow",
            "primary_keyword": "Parkside Tavern Morristown"
        }

    # ============================================================
    # 6. SEO LANDING PAGE DATA
    # ============================================================

    def build_landing_page(self, slug: str) -> Optional[Dict[str, Any]]:
        config = self.get_page_config(slug)

        if not config:
            return None

        intent = config["intent"]
        cta = self.get_cta_for_intent(
            "private_event" if intent == "private_event" else "general"
        )

        if slug in ["cocktails", "happy-hour"]:
            cta = self.get_cta_for_intent("drinks")

        if slug in ["dinner", "brunch"]:
            cta = self.get_cta_for_intent("food")

        meta = self.build_meta_tags(slug)

        return {
            "slug": slug,
            "title": config["title"],
            "headline": self.build_headline(config),
            "subheadline": self.build_subheadline(config),
            "primary_keyword": config["primary_keyword"],
            "meta": meta,
            "content_sections": self.build_content_sections(slug, config),
            "cta": cta,
            "official_links": self.get_official_links(),
            "privacy_note": (
                "ParksideAI does not take reservations or collect guest information. "
                "Guests are routed to official Parkside Tavern links."
            ),
            "schema": self.build_structured_data(slug, config),
            "seo_rules": settings.SEO_PAGE_RULES
        }

    def build_headline(self, config: Dict[str, Any]) -> str:
        return f"{config['title']} at {self.restaurant_name} in {self.city}, {self.state}"

    def build_subheadline(self, config: Dict[str, Any]) -> str:
        keyword = config["primary_keyword"]

        return (
            f"Discover {keyword} with {self.restaurant_name}, a Morristown tavern "
            f"and cocktail bar located near {settings.RESTAURANT_NEIGHBORHOOD}."
        )

    def build_content_sections(
        self,
        slug: str,
        config: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        title = config["title"]
        keyword = config["primary_keyword"]

        sections = [
            {
                "heading": f"{title} in {self.city}",
                "body": (
                    f"{self.restaurant_name} is a local destination for {keyword}. "
                    f"Guests can explore official Parkside Tavern information through "
                    f"the restaurant website and use official booking or inquiry links "
                    f"when appropriate."
                )
            },
            {
                "heading": "Official Parkside Tavern Information",
                "body": (
                    f"ParksideAI is designed to guide guests to official Parkside Tavern "
                    f"resources. For menus, hours, drinks, brunch, and general restaurant "
                    f"details, guests should use the official website."
                )
            },
            {
                "heading": "Privacy-Safe Guest Routing",
                "body": (
                    f"ParksideAI does not take reservations directly and does not collect "
                    f"guest personal information. Reservation guests are routed to OpenTable, "
                    f"and private event guests are routed to the official Tripleseat inquiry form."
                )
            }
        ]

        if config["intent"] == "private_event":
            sections.append({
                "heading": "Private Events and Group Gatherings",
                "body": (
                    f"For {keyword}, guests should use the official Parkside Tavern private "
                    f"event inquiry form. This helps ensure availability, event details, and "
                    f"planning information are handled through the correct official channel."
                )
            })

        return sections

    # ============================================================
    # 7. STRUCTURED DATA
    # ============================================================

    def build_structured_data(
        self,
        slug: str = "general",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        schema = dict(settings.STRUCTURED_DATA_DEFAULTS)

        schema["description"] = settings.SEO_DEFAULT_DESCRIPTION
        schema["sameAs"] = [
            self.main_website,
            self.reservation_link,
            self.private_events_link
        ]

        if config:
            schema["name"] = f"{self.restaurant_name} - {config['title']}"
            schema["keywords"] = [
                config["primary_keyword"],
                *settings.SEO_PRIMARY_KEYWORDS[:8]
            ]

        return schema

    # ============================================================
    # 8. SEO API PAYLOADS
    # ============================================================

    def build_seo_index_payload(self) -> Dict[str, Any]:
        return {
            "success": True,
            "service": "ParksideAI SEO Engine",
            "restaurant": self.restaurant_name,
            "location": settings.LOCAL_SEO_IDENTITY,
            "available_pages": self.list_available_pages(),
            "primary_keywords": settings.SEO_PRIMARY_KEYWORDS,
            "location_targets": settings.SEO_LOCATION_TARGETS,
            "official_links": self.get_official_links(),
            "privacy_mode": settings.PRIVACY_MODE
        }

    def build_page_not_found_payload(self, slug: str) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "seo_page_not_found",
            "slug": slug,
            "available_pages": self.list_available_pages()
        }


seo_service = SEOService()