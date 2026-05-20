import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "ParksideAI")
    RESTAURANT_NAME = os.getenv("RESTAURANT_NAME", "Parkside Tavern")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    LEAD_KEYWORDS = [
        "private event",
        "party",
        "birthday",
        "reservation",
        "book",
        "corporate",
        "holiday party",
        "large group",
        "catering",
        "wedding",
        "brunch",
        "fundraiser",
    ]


settings = Settings()