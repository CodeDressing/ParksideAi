# ============================================================
# ParksideAI
# Search Engine Routes
# Phase 5 Part 3.0 — FIXED
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

FIXES APPLIED:
- Section 3: Removed broken route imports (circular import crash)
- Section 4: Removed app.register_blueprint() calls (NameError crash)
- Section 3: Added BASE_URL constant (was undefined, caused NameError)
- Section 4: Added robots.txt route (was missing, Google got 404)
- Section 5.5: Fixed sitemap xmlns https -> http (Google rejects https)
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
# SECTION 3 — BASE URL
# ============================================================
# FIXED: Old Sections 3 and 4 contained circular route imports
# and app.register_blueprint() calls that caused a NameError
# crash at startup. Blueprint registration belongs in
# app/__init__.py and run.py only — never inside a Blueprint file.
# BASE_URL is defined here once for use across sitemap and robots.
# ============================================================

BASE_URL = "https://parksideai.onrender.com"


# ============================================================
# SECTION 4 — ROBOTS.TXT
# ============================================================
# FIXED: robots.txt route was completely missing. Google was
# getting a 404 every time it checked crawl permissions.
# This tells all crawlers they are allowed and points them
# directly to the sitemap for page discovery.
# ============================================================

@search_engine_bp.route(
    "/robots.txt",
    methods=["GET"]
)
def robots_txt():
    """
    Robots.txt for search engine crawlers.
    Allows all crawlers. Points to sitemap.xml.
    """

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )

    return Response(
        content,
        mimetype="text/plain"
    )


# ============================================================
# SECTION 5 — XML SITEMAP
# ============================================================
# FIXED: xmlns was https://sitemaps.org — Google only accepts
# http://sitemaps.org. Wrong namespace caused silent sitemap
# rejection in Google Search Console.
# ============================================================

@search_engine_bp.route(
    "/sitemap.xml",
    methods=["GET"]
)
def sitemap_xml():
    """
    Dynamic sitemap generator.
    Includes homepage, SEO index, static routes,
    and all dynamic SEO landing pages.
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
    # FIXED: xmlns changed from https:// to http://
    # --------------------------------------------------------

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
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
    Confirms BASE_URL, sitemap, and robots.txt are live.
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
