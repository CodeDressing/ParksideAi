"""
============================================================
ParksideAI
SEO Intelligence Engine
Phase 5 Part 1.0
============================================================

Responsibilities:
- SEO landing page generation
- local hospitality SEO
- semantic page clustering
- related page discovery
- structured data generation
- metadata generation
- future AI ranking support
- future embedding compatibility
"""

# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from config.settings import settings


# ============================================================
# SECTION 2 — SEO SERVICE CLASS
# ============================================================

class SEOService:

    def __init__(self):

        self.restaurant_name = (
            settings.RESTAURANT_NAME
        )

        self.city = (
            settings.RESTAURANT_CITY
        )

        self.state = (
            settings.RESTAURANT_STATE
        )

        self.region = (
            settings.RESTAURANT_REGION
        )

        self.address = (
            settings.RESTAURANT_ADDRESS
        )

        self.main_website = (
            settings.OFFICIAL_MAIN_WEBSITE
        )

        self.reservation_link = (
            settings.OFFICIAL_RESERVATION_LINK
        )

        self.private_events_link = (
            settings.OFFICIAL_PRIVATE_EVENTS_LINK
        )

        self.food_menu_link = (
            settings.OFFICIAL_FOOD_MENU_LINK
        )

        self.drink_menu_link = (
            settings.OFFICIAL_DRINK_MENU_LINK
        )


    # ========================================================
    # SECTION 3 — INTENT DETECTION
    # ========================================================

    def detect_seo_intent(
        self,
        query: str
    ) -> str:

        query_lower = (
            query or ""
        ).lower()

        if any(

            keyword in query_lower

            for keyword in
            settings.RESERVATION_KEYWORDS
        ):

            return "reservation"

        if any(

            keyword in query_lower

            for keyword in
            settings.PRIVATE_EVENT_KEYWORDS
        ):

            return "private_event"

        if any(

            keyword in query_lower

            for keyword in
            settings.RESTAURANT_INFO_KEYWORDS
        ):

            return "restaurant_info"

        return "general"


    # ========================================================
    # SECTION 4 — OFFICIAL LINKS
    # ========================================================

    def get_official_links(self) -> Dict[str, str]:

        return {

            "main_website":
                self.main_website,

            "reservations":
                self.reservation_link,

            "private_events":
                self.private_events_link,

            "food_menu":
                self.food_menu_link,

            "drink_menu":
                self.drink_menu_link
        }


    # ========================================================
    # SECTION 5 — SEMANTIC TOPICS
    # ========================================================

    def get_semantic_topics(self) -> List[str]:

        return [

            "Morristown dining",

            "Morristown nightlife",

            "cocktail destination",

            "private events",

            "group dining",

            "sports viewing",

            "brunch destination",

            "happy hour destination",

            "restaurant near Headquarters Plaza",

            "Morris County hospitality",

            "cocktail bar in Morristown",

            "local tavern experience",

            "social dining experience",

            "group hospitality"
        ]


    # ========================================================
    # SECTION 6 — KEYWORD CONTEXT
    # ========================================================

    def generate_keyword_context(
        self,
        user_query: str = ""
    ) -> Dict[str, Any]:

        return {

            "restaurant":
                self.restaurant_name,

            "location": {

                "city":
                    self.city,

                "state":
                    self.state,

                "region":
                    self.region,

                "address":
                    self.address,

                "neighborhood":
                    settings.RESTAURANT_NEIGHBORHOOD
            },

            "primary_keywords":
                settings.SEO_PRIMARY_KEYWORDS,

            "location_targets":
                settings.SEO_LOCATION_TARGETS,

            "semantic_topics":
                self.get_semantic_topics(),

            "query_intent":
                self.detect_seo_intent(
                    user_query
                ),

            "official_links":
                self.get_official_links(),

            "privacy_mode":
                settings.PRIVACY_MODE
        }


    # ========================================================
    # SECTION 7 — PAGE CONFIG
    # ========================================================

    def get_page_config(
        self,
        slug: str
    ) -> Optional[Dict[str, Any]]:

        return (
            settings.SEO_SERVICE_CATEGORIES.get(
                slug
            )
        )


    # ========================================================
    # SECTION 8 — PAGE LISTING
    # ========================================================

    def list_available_pages(
        self
    ) -> List[Dict[str, Any]]:

        pages = []

        for slug, config in (
            settings.SEO_SERVICE_CATEGORIES.items()
        ):

            pages.append({

                "slug":
                    slug,

                "title":
                    config["title"],

                "primary_keyword":
                    config["primary_keyword"],

                "intent":
                    config["intent"],

                "url_path":
                    f"/seo/{slug}",

                "official_link":
                    config["official_link"]
            })

        return pages


    # ========================================================
    # SECTION 9 — RELATED PAGE ENGINE
    # ========================================================
    # ========================================================
    # SECTION 9 — DYNAMIC RELATED PAGE ENGINE
    # Phase 6 Part 9.1.2 — Dynamic Link Scoring
    # ========================================================

    def get_related_pages(
        self,
        slug: str
    ) -> List[Dict[str, Any]]:

        pages = self.list_available_pages()

        current_page = self.get_page_config(slug)

        if not current_page:
            return []

        scored_pages = []

        current_intent = current_page["intent"]
        current_cluster = self.get_cluster_for_slug(slug)

        popular_slugs = [

            "lunch",
            "private-events",
            "business-lunch-morristown",
            "restaurants-near-headquarters-plaza",
            "restaurants-near-hyatt-regency-morristown",
            "birthday-parties",
            "corporate-events",
            "cocktails",
            "brunch",
            "group-dining"
        ]

        location_slugs = [

            "restaurants-near-headquarters-plaza",
            "restaurants-near-hyatt-regency-morristown",
            "restaurants-near-morristown-green",
            "downtown-morristown-restaurant",
            "restaurants-near-mayo-performing-arts-center",
            "bars-near-headquarters-plaza",
            "nightlife-morristown",
            "sports-bar-morristown"
        ]

        for page in pages:

            if page["slug"] == slug:
                continue

            score = 0

            page_cluster = self.get_cluster_for_slug(
                page["slug"]
            )

            if current_cluster and page_cluster == current_cluster:
                score += 100

            if page["intent"] == current_intent:
                score += 50

            if page["slug"] in location_slugs and slug in location_slugs:
                score += 40

            if page["slug"] in popular_slugs:
                score += 20

            if self.city.lower() in page["primary_keyword"].lower():
                score += 10

            if score > 0:

                scored_pages.append({
                    **page,
                    "related_score": score
                })

        scored_pages.sort(
            key=lambda page: page["related_score"],
            reverse=True
        )

        return scored_pages[:10]


    # ========================================================
    # SECTION 9.1 — CLUSTER LOOKUP ENGINE
    # Phase 6 Part 9.1.2
    # ========================================================

    def get_cluster_for_slug(
        self,
        slug: str
    ) -> Optional[str]:

        for cluster_name, cluster_slugs in self.SEO_CLUSTERS.items():

            if slug in cluster_slugs:
                return cluster_name

        return None
    # ============================================================
    # SECTION 9.5 — SEO CLUSTERS
    # Phase 6 Part 6.0
    # ============================================================

    SEO_CLUSTERS = {

        "lunch": [

            "lunch",
            "business-lunch-morristown",
            "lunch-near-headquarters-plaza",
            "weekday-lunch-morristown",
            "lunch-meeting-restaurant",
            "lunch-cocktails-morristown"
        ],

        "events": [

            "private-events",
            "birthday-parties",
            "corporate-events",
            "holiday-parties",
            "group-dining",
            "rehearsal-dinners",
            "retirement-parties",
            "networking-events",
            "team-dinners",
            "graduation-parties"
        ],

        "morristown": [

            "sports-bar-morristown",
            "bars-near-headquarters-plaza",
            "nightlife-morristown"
        ]
    }


    # ========================================================
    # SECTION 10 — CTA ENGINE
    # ========================================================

    def get_cta_for_intent(
        self,
        intent: str
    ) -> Dict[str, str]:

        if intent == "reservation":

            return {

                "label":
                    "Book on OpenTable",

                "url":
                    self.reservation_link,

                "type":
                    "official_reservation_link"
            }

        if intent == "private_event":

            return {

                "label":
                    "Submit Private Event Inquiry",

                "url":
                    self.private_events_link,

                "type":
                    "official_private_event_link"
            }

        if intent == "drinks":

            return {

                "label":
                    "View Drink Menu",

                "url":
                    self.drink_menu_link,

                "type":
                    "official_menu_link"
            }

        if intent == "food":

            return {

                "label":
                    "View Food Menu",

                "url":
                    self.food_menu_link,

                "type":
                    "official_menu_link"
            }

        return {

            "label":
                "Visit Official Website",

            "url":
                self.main_website,

            "type":
                "official_website_link"
        }


    # ========================================================
    # SECTION 11 — META TAG ENGINE
    # ========================================================

    def build_meta_tags(
        self,
        page_type: str = "general"
    ) -> Dict[str, str]:

        config = (
            self.get_page_config(page_type)
        )

        if config:

            title = (
                f"{config['title']} "
                f"in {self.city} NJ"
                f"{settings.SEO_DEFAULT_TITLE_SUFFIX}"
            )

            description = (

                f"Explore "
                f"{config['primary_keyword']} "
                f"with {self.restaurant_name}. "
                f"Find official Parkside Tavern "
                f"information, menus, cocktails, "
                f"private events, and hospitality "
                f"details in Morristown NJ."
            )

            return {

                "title":
                    title,

                "description":
                    description[:300],

                "canonical":
                    self.main_website,

                "robots":
                    "index, follow",

                "primary_keyword":
                    config["primary_keyword"]
            }

        return {

            "title":
                (
                    f"{self.restaurant_name} "
                    f"| {self.city} NJ Restaurant"
                ),

            "description":
                settings.SEO_DEFAULT_DESCRIPTION,

            "canonical":
                self.main_website,

            "robots":
                "index, follow",

            "primary_keyword":
                "Parkside Tavern Morristown"
        }


    # ========================================================
    # SECTION 12 — LANDING PAGE ENGINE
    # ========================================================

    def build_landing_page(
        self,
        slug: str
    ) -> Optional[Dict[str, Any]]:

        config = (
            self.get_page_config(slug)
        )

        if not config:
            return None

        intent = (
            config["intent"]
        )

        cta = self.get_cta_for_intent(

            "private_event"

            if intent == "private_event"

            else "general"
        )

        if slug in [
            "cocktails",
            "happy-hour"
        ]:

            cta = (
                self.get_cta_for_intent(
                    "drinks"
                )
            )

        if slug in [
            "dinner",
            "brunch"
        ]:

            cta = (
                self.get_cta_for_intent(
                    "food"
                )
            )

        return {

            "slug":
                slug,

            "title":
                config["title"],

            "headline":
                self.build_headline(
                    config
                ),

            "subheadline":
                self.build_subheadline(
                    config
                ),

            "primary_keyword":
                config["primary_keyword"],

            "meta":
                self.build_meta_tags(slug),

            "content_sections":
                 self.build_content_sections(
                    slug,
                     config
                 ),

            "related_pages":
                  self.get_related_pages(
                     slug
                 ),

            "cta":
                 cta,

            "official_links":
                self.get_official_links(),

            "privacy_note":
                (
                    "ParksideAI does not take "
                    "reservations or collect "
                    "guest information."
                ),

            "schema":
                self.build_structured_data(
                    slug,
                    config
                ),

            "seo_rules":
                settings.SEO_PAGE_RULES
        }


    # ========================================================
    # SECTION 13 — HEADLINE ENGINE
    # ========================================================

    def build_headline(
        self,
        config: Dict[str, Any]
    ) -> str:

        return (

            f"{config['title']} "
            f"at {self.restaurant_name} "
            f"in {self.city}, "
            f"{self.state}"
        )


    # ========================================================
    # SECTION 14 — SUBHEADLINE ENGINE
    # ========================================================

    def build_subheadline(
        self,
        config: Dict[str, Any]
    ) -> str:

        keyword = (
            config["primary_keyword"]
        )

        return (

            f"Discover {keyword} "
            f"with {self.restaurant_name}, "
            f"a Morristown tavern and "
            f"cocktail destination near "
            f"{settings.RESTAURANT_NEIGHBORHOOD}."
        )


    # ========================================================
    # SECTION 15 — CONTENT ENGINE
    # ========================================================

    def build_content_sections(
        self,
        slug: str,
        config: Dict[str, Any]
    ) -> List[Dict[str, str]]:

        title = config["title"]

        keyword = (
            config["primary_keyword"]
        )

        sections = [

            {
                "heading":
                    f"{title} in {self.city}",

                "body":
                    self.build_dynamic_page_intro(
                        slug,
                        keyword
                    )
            },

            {
                "heading":
                    "Official Hospitality Information",

                "body":
                    (
                        "ParksideAI is designed "
                        "to guide guests to official "
                        "Parkside Tavern resources "
                        "including OpenTable, "
                        "Tripleseat, and "
                        "parksidenj.com."
                    )
            },

            {
                "heading":
                    "Privacy-Safe Guest Experience",

                "body":
                    (
                        "ParksideAI does not take "
                        "reservations directly and "
                        "does not collect guest "
                        "personal information."
                    )
            }
        ]

        if config["intent"] == "private_event":

            sections.append({

                "heading":
                    "Private Event Routing",

                "body":
                    (
                        "Private event and group "
                        "inquiries are routed through "
                        "the official Parkside Tavern "
                        "Tripleseat platform."
                    )
            })

        return sections



    # ========================================================
    # SECTION 15.1 — DYNAMIC INTRO ENGINE
    # ========================================================
    # ========================================================
    # SECTION 15.1 — DYNAMIC INTRO ENGINE
    # Phase 6.7 + 6.8 Super Upgrade
    # ========================================================

    def build_dynamic_page_intro(
            self,
            slug: str,
            keyword: str
    ) -> str:

        intro_map = {

            # ==================================================
            # LUNCH CLUSTER
            # ==================================================

            "lunch":
                (
                    f"{self.restaurant_name} offers lunch in "
                    f"{self.city} for professionals, visitors, "
                    f"hotel guests, and locals looking for food, "
                    f"cocktails, and hospitality near "
                    f"Headquarters Plaza."
                ),

            "business-lunch-morristown":
                (
                    f"{self.restaurant_name} offers business lunch "
                    f"experiences in {self.city} for meetings, "
                    f"networking, client entertainment, and "
                    f"professional dining."
                ),

            "lunch-near-headquarters-plaza":
                (
                    f"Guests searching for lunch near "
                    f"Headquarters Plaza can discover food, "
                    f"cocktails, and hospitality at "
                    f"{self.restaurant_name}."
                ),

            "weekday-lunch-morristown":
                (
                    f"{self.restaurant_name} serves weekday lunch "
                    f"in {self.city} for professionals, visitors, "
                    f"and guests seeking a downtown dining option."
                ),

            "lunch-meeting-restaurant":
                (
                    f"{self.restaurant_name} provides a lunch "
                    f"meeting destination for business guests, "
                    f"corporate lunches, and professional gatherings."
                ),

            "lunch-cocktails-morristown":
                (
                    f"{self.restaurant_name} combines lunch, "
                    f"cocktails, hospitality, and social dining "
                    f"in downtown {self.city}."
                ),

            # ==================================================
            # EVENT CLUSTER
            # ==================================================

            "birthday-parties":
                (
                    f"{self.restaurant_name} hosts birthday "
                    f"celebrations in {self.city} with dining, "
                    f"cocktails, hospitality, and group experiences."
                ),

            "rehearsal-dinners":
                (
                    f"Guests planning rehearsal dinners in "
                    f"{self.city} can explore hospitality and "
                    f"group dining experiences at "
                    f"{self.restaurant_name}."
                ),

            "corporate-events":
                (
                    f"{self.restaurant_name} supports corporate "
                    f"events, business gatherings, networking "
                    f"functions, and professional hospitality."
                ),

            "holiday-parties":
                (
                    f"{self.restaurant_name} provides holiday "
                    f"party experiences for organizations, "
                    f"friends, families, and businesses."
                ),

            "retirement-parties":
                (
                    f"Guests planning retirement celebrations "
                    f"in {self.city} can explore food, drinks, "
                    f"and hospitality at {self.restaurant_name}."
                ),

            "networking-events":
                (
                    f"{self.restaurant_name} offers networking "
                    f"event opportunities for professionals and "
                    f"organizations throughout Morris County."
                ),

            "team-dinners":
                (
                    f"{self.restaurant_name} provides team dinner "
                    f"experiences for businesses, organizations, "
                    f"and social groups."
                ),

            "graduation-parties":
                (
                    f"{self.restaurant_name} hosts graduation "
                    f"celebrations for families, students, "
                    f"friends, and community gatherings."
                ),

            # ==================================================
            # EXISTING CORE PAGES
            # ==================================================

            "private-events":
                (
                    f"{self.restaurant_name} offers private event "
                    f"experiences in {self.city} for birthdays, "
                    f"corporate gatherings, holiday parties, and "
                    f"group celebrations."
                ),

            "brunch":
                (
                    f"Guests exploring brunch in {self.city} can "
                    f"discover cocktails, hospitality, and weekend "
                    f"dining experiences at {self.restaurant_name}."
                ),

            "happy-hour":
                (
                    f"{self.restaurant_name} offers happy hour and "
                    f"cocktail-focused hospitality experiences in "
                    f"{self.city}, {self.state}."
                ),

            "cocktails":
                (
                    f"{self.restaurant_name} is a Morristown "
                    f"cocktail destination offering drinks, "
                    f"nightlife, social dining, and hospitality."
                ),

            "group-dining":
                (
                    f"Guests searching for group dining in "
                    f"{self.city} can explore food, cocktails, "
                    f"celebrations, and hospitality experiences "
                    f"with {self.restaurant_name}."
                )
        }

        return intro_map.get(

            slug,

            (
                f"{self.restaurant_name} provides "
                f"{keyword} experiences in "
                f"{self.city}, {self.state}."
            )
        )
    # ========================================================
    # SECTION 16 — STRUCTURED DATA
    # ========================================================
    # ========================================================
    # SECTION 16 — STRUCTURED DATA GRAPH ENGINE
    # Phase 6 Part 9.1.0 — Schema Graph Upgrade
    # ========================================================

    def build_structured_data(
        self,
        slug: str = "general",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        page_title = (
            config["title"]
            if config
            else self.restaurant_name
        )

        primary_keyword = (
            config["primary_keyword"]
            if config
            else "Parkside Tavern Morristown"
        )

        page_url = (
            f"https://parksideai.onrender.com/seo/{slug}"
        )

        page_description = (
            f"Explore {primary_keyword} with "
            f"{self.restaurant_name} in "
            f"{self.city}, {self.state}."
        )

        organization_id = (
            f"{self.main_website}#organization"
        )

        restaurant_id = (
            f"{self.main_website}#restaurant"
        )

        website_id = (
            "https://parksideai.onrender.com/#website"
        )

        webpage_id = (
            f"{page_url}#webpage"
        )

        faq_id = (
            f"{page_url}#faq"
        )

        breadcrumb_id = (
            f"{page_url}#breadcrumb"
        )

        organization_schema = {
            "@type": "Organization",
            "@id": organization_id,
            "name": self.restaurant_name,
            "url": self.main_website,
            "sameAs": [
                self.main_website,
                self.reservation_link,
                self.private_events_link
            ]
        }

        restaurant_schema = {
            "@type": [
                "Restaurant",
                "LocalBusiness"
            ],
            "@id": restaurant_id,
            "name": self.restaurant_name,
            "url": self.main_website,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "9 Speedwell Ave",
                "addressLocality": self.city,
                "addressRegion": self.state,
                "postalCode": "07960",
                "addressCountry": "US"
            },
            "servesCuisine": "American",
            "priceRange": "$$",
            "parentOrganization": {
                "@id": organization_id
            },
            "sameAs": [
                self.main_website,
                self.reservation_link,
                self.private_events_link
            ]
        }

        website_schema = {
            "@type": "WebSite",
            "@id": website_id,
            "name": "ParksideAI",
            "url": "https://parksideai.onrender.com/",
            "publisher": {
                "@id": organization_id
            },
            "about": {
                "@id": restaurant_id
            }
        }

        webpage_schema = {
            "@type": "WebPage",
            "@id": webpage_id,
            "url": page_url,
            "name": (
                f"{page_title} | "
                f"{self.restaurant_name} "
                f"{self.city} {self.state}"
            ),
            "description": page_description,
            "isPartOf": {
                "@id": website_id
            },
            "about": {
                "@id": restaurant_id
            },
            "mainEntity": {
                "@id": faq_id
            },
            "breadcrumb": {
                "@id": breadcrumb_id
            },
            "keywords": [
                primary_keyword,
                *settings.SEO_PRIMARY_KEYWORDS[:8]
            ]
        }

        faq_schema = {
            "@type": "FAQPage",
            "@id": faq_id,
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Does Parkside Tavern take reservations?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": (
                            "Yes. Guests can make official reservations "
                            "through Parkside Tavern's OpenTable platform. "
                            "ParksideAI does not take reservations directly."
                        )
                    }
                },
                {
                    "@type": "Question",
                    "name": "Does Parkside Tavern host private events?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": (
                            "Yes. Parkside Tavern offers private event "
                            "and group dining inquiries through the "
                            "official Tripleseat platform."
                        )
                    }
                },
                {
                    "@type": "Question",
                    "name": "Where is Parkside Tavern located?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": (
                            "Parkside Tavern is located at "
                            "9 Speedwell Ave in Morristown, New Jersey, "
                            "near Headquarters Plaza."
                        )
                    }
                },
                {
                    "@type": "Question",
                    "name": "Does Parkside Tavern offer food, drinks, brunch, lunch, and cocktails?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": (
                            "Yes. Parkside Tavern offers food, drinks, "
                            "brunch, lunch discovery, cocktails, and "
                            "hospitality-focused dining experiences "
                            "in Morristown NJ."
                        )
                    }
                }
            ]
        }

        breadcrumb_schema = {
            "@type": "BreadcrumbList",
            "@id": breadcrumb_id,
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": self.main_website
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "SEO Pages",
                    "item": "https://parksideai.onrender.com/seo/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page_title,
                    "item": page_url
                }
            ]
        }

        return {
            "@context": "https://schema.org",
            "@graph": [
                organization_schema,
                restaurant_schema,
                website_schema,
                webpage_schema,
                faq_schema,
                breadcrumb_schema
            ]
        }
    # ========================================================
    # SECTION 17 — SEO INDEX PAYLOAD
    # ========================================================

    def build_seo_index_payload(
        self
    ) -> Dict[str, Any]:

        return {

            "success": True,

            "service":
                "ParksideAI SEO Engine",

            "restaurant":
                self.restaurant_name,

            "location":
                settings.LOCAL_SEO_IDENTITY,

            "available_pages":
                self.list_available_pages(),

            "primary_keywords":
                settings.SEO_PRIMARY_KEYWORDS,

            "location_targets":
                settings.SEO_LOCATION_TARGETS,

            "official_links":
                self.get_official_links(),

            "privacy_mode":
                settings.PRIVACY_MODE
        }


    # ========================================================
    # SECTION 18 — PAGE NOT FOUND
    # ========================================================

    def build_page_not_found_payload(
        self,
        slug: str
    ) -> Dict[str, Any]:

        return {

            "success": False,

            "error":
                "seo_page_not_found",

            "slug":
                slug,

            "available_pages":
                self.list_available_pages()
        }


# ============================================================
# SECTION 19 — SERVICE INSTANCE
# ============================================================

seo_service = SEOService()