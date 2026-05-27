# ============================================================
# ParksideAI
# Search Engine Routes
# Phase 5 Part 2.5
# ============================================================

"""
Search Engine Infrastructure

Responsibilities:
- robots.txt generation
- sitemap.xml generation
- SEO discovery support
- crawler accessibility
- search engine indexing
- sitemap scalability
- URL discovery infrastructure
"""

# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

from flask import Blueprint
from flask import Response

from services.seo_service import seo_service
from config.settings import settings


# ============================================================
# SECTION 2 — BLUEPRINT SETUP
# ============================================================

search_engine_bp = Blueprint(
    "search_engine",
    __name__
)


# ============================================================
# SECTION 3 — CORE DOMAIN CONFIGURATION
# ============================================================

BASE_URL = (
    "https://parksideai.onrender.com"
)


# ============================================================
# SECTION 4 — ROBOTS.TXT
# ============================================================

@search_engine_bp.route(
    "/robots.txt",
    methods=["GET"]
)
def robots_txt():
    """
    Public crawler instructions.
    """

    sitemap_url = (
        f"{BASE_URL}/sitemap.xml"
    )

    content = f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""

    return Response(
        content,
        mimetype="text/plain"
    )


# ============================================================
# SECTION 5 — XML SITEMAP
# ============================================================

@search_engine_bp.route(
    "/sitemap.xml",
    methods=["GET"]
)
def sitemap_xml():
    """
    Dynamic sitemap generator.
    """

    # --------------------------------------------------------
    # SUBSECTION 5.1 — SEO PAGE DISCOVERY
    # --------------------------------------------------------

    pages = (
        seo_service.list_available_pages()
    )

    # --------------------------------------------------------
    # SUBSECTION 5.2 — CORE STATIC URLS
    # --------------------------------------------------------

    urls = [

        f"{BASE_URL}/",

        f"{BASE_URL}/seo/",

        f"{BASE_URL}/seo/reservations",

        f"{BASE_URL}/seo/menu"
    ]

    # --------------------------------------------------------
    # SUBSECTION 5.3 — DYNAMIC SEO URLS
    # --------------------------------------------------------

    for page in pages:

        urls.append(
            f"{BASE_URL}/seo/{page['slug']}"
        )

    # --------------------------------------------------------
    # SUBSECTION 5.4 — XML URL GENERATION
    # --------------------------------------------------------

    xml_items = ""

    for url in urls:

        xml_items += f"""
    <url>
        <loc>{url}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

    # --------------------------------------------------------
    # SUBSECTION 5.5 — XML DOCUMENT BUILD
    # --------------------------------------------------------

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>
"""

    # --------------------------------------------------------
    # SUBSECTION 5.6 — XML RESPONSE
    # --------------------------------------------------------

    return Response(
        sitemap,
        mimetype="application/xml"
    )


# ============================================================
# SECTION 6 — SEARCH ENGINE HEALTH
# ============================================================

@search_engine_bp.route(
    "/search-health",
    methods=["GET"]
)
def search_engine_health():
    """
    Search engine infrastructure health check.
    """

    return {

        "success": True,

        "engine":
            "ParksideAI Search Engine Infrastructure",

        "base_url":
            BASE_URL,

        "seo_pages":
            len(
                seo_service.list_available_pages()
            ),

        "robots":
            f"{BASE_URL}/robots.txt",

        "sitemap":
            f"{BASE_URL}/sitemap.xml"
    }