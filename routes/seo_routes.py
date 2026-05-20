"""
SEO Routes - Dynamic landing pages for search engines
Phase 3
"""

from flask import Blueprint, jsonify, render_template_string
from config.settings import settings

seo_bp = Blueprint("seo", __name__, url_prefix="/seo")


@seo_bp.route("/")
def seo_home():
    """SEO endpoint status"""
    return jsonify({
        "service": "ParksideAI SEO Engine",
        "status": "online",
        "restaurant": settings.RESTAURANT_NAME,
        "privacy_mode": "no_guest_data_collection"
    })


@seo_bp.route("/reservations")
def seo_reservations():
    """SEO landing page for reservation queries"""
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Parkside Tavern Reservations | Morristown NJ</title>
            <meta name="description" content="Make reservations at Parkside Tavern in Morristown, NJ through OpenTable.">
            <meta http-equiv="refresh" content="0; url=https://www.opentable.com/r/parkside-tavern-morristown">
        </head>
        <body>
            <p>Redirecting to Parkside Tavern reservations on OpenTable...</p>
        </body>
        </html>
    """)


@seo_bp.route("/private-events")
def seo_private_events():
    """SEO landing page for private event queries"""
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Private Events at Parkside Tavern | Morristown NJ</title>
            <meta name="description" content="Host birthday parties, corporate events, and celebrations at Parkside Tavern.">
            <meta http-equiv="refresh" content="0; url=https://parksidetavern.tripleseat.com/party_request/45075">
        </head>
        <body>
            <p>Redirecting to Parkside Tavern private events inquiry form...</p>
        </body>
        </html>
    """)


@seo_bp.route("/menu")
def seo_menu():
    """SEO landing page for menu queries"""
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Parkside Tavern Menu | Morristown NJ</title>
            <meta name="description" content="View Parkside Tavern food and drink menus in Morristown, NJ.">
            <meta http-equiv="refresh" content="0; url=https://parksidenj.com/morristown-morristown-parkside-tavern-food-menu">
        </head>
        <body>
            <p>Redirecting to Parkside Tavern menu...</p>
        </body>
        </html>
    """)