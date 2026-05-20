"""
SEO Service - Generate semantic content for search engines
Phase 3
"""

from typing import Dict, List, Any
from config.settings import settings


class SEOService:
    """Generate SEO-optimized content for Parkside Tavern"""

    def __init__(self):
        self.restaurant_name = settings.RESTAURANT_NAME
        self.location = "Morristown, NJ"

    def generate_keyword_context(self, user_query: str) -> Dict[str, Any]:
        """Extract and return SEO keywords from query"""
        keywords = {
            "primary": ["Parkside Tavern", "Morristown restaurant", "Morristown tavern"],
            "secondary": ["cocktail bar", "brunch", "happy hour", "private events"],
            "location_specific": ["Headquarters Plaza", "Morris County", "downtown Morristown"],
            "query_intent": self._detect_intent(user_query)
        }
        return keywords

    def _detect_intent(self, query: str) -> str:
        """Detect SEO intent category"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["reservation", "book", "table"]):
            return "reservation"
        elif any(word in query_lower for word in ["private event", "party", "birthday", "corporate"]):
            return "private_event"
        elif any(word in query_lower for word in ["menu", "food", "drink", "cocktail"]):
            return "menu"
        elif any(word in query_lower for word in ["hours", "open", "close"]):
            return "hours"
        else:
            return "general"

    def get_semantic_topics(self) -> List[str]:
        """Return core semantic topics for SEO"""
        return [
            "Morristown dining",
            "cocktail destination",
            "local tavern",
            "group dining",
            "event venue",
            "social dining experience",
            "sports viewing",
            "brunch destination",
            "nightlife",
            "restaurant near Headquarters Plaza"
        ]

    def build_meta_tags(self, page_type: str = "general") -> Dict[str, str]:
        """Generate meta tags for SEO pages"""
        base_description = f"{self.restaurant_name} is an old world tavern and cocktail bar located in {self.location}."

        meta = {
            "general": {
                "title": f"{self.restaurant_name} | {self.location}",
                "description": base_description + " Enjoy brunch, dinner, cocktails, and private events."
            },
            "reservation": {
                "title": f"{self.restaurant_name} Reservations | {self.location}",
                "description": "Book your table at Parkside Tavern through OpenTable. Reserve for dinner, brunch, or happy hour."
            },
            "private_event": {
                "title": f"Private Events at {self.restaurant_name} | {self.location}",
                "description": "Host birthday parties, corporate events, and celebrations at Parkside Tavern. Submit an inquiry today."
            }
        }

        return meta.get(page_type, meta["general"])


# Singleton instance
seo_service = SEOService()