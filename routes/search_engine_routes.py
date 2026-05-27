# ============================================================
# ParksideAI
# Search Engine Routes
# Phase 5 Part 2.2
# ============================================================

from flask import Blueprint, Response

from services.seo_service import seo_service
from config.settings import settings


search_engine_bp = Blueprint(
    "search_engine",
    __name__
)


@search_engine_bp.route("/robots.txt", methods=["GET"])
def robots_txt():
    sitemap_url = "https://parksideai.onrender.com/sitemap.xml"

    content = f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""

    return Response(
        content,
        mimetype="text/plain"
    )


@search_engine_bp.route("/sitemap.xml", methods=["GET"])
def sitemap_xml():
    pages = seo_service.list_available_pages()

    urls = [
        "https://parksideai.onrender.com/",
        "https://parksideai.onrender.com/seo/"
    ]

    for page in pages:
        urls.append(
            f"https://parksideai.onrender.com/seo/{page['slug']}"
        )

    xml_items = ""

    for url in urls:
        xml_items += f"""
    <url>
        <loc>{url}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>
"""

    return Response(
        sitemap,
        mimetype="application/xml"
    )