import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App Identity
    APP_NAME = os.getenv("APP_NAME", "ParksideAI")
    RESTAURANT_NAME = os.getenv("RESTAURANT_NAME", "Parkside Tavern")

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Note: gpt-4.1-mini doesn't exist, using gpt-4o-mini
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "500"))

    # Flask
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "parkside-production-key-change-this")

    # File Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    KNOWLEDGE_FILE = os.getenv("KNOWLEDGE_FILE", os.path.join(BASE_DIR, "data", "parkside_knowledge.json"))

    # Lead/Intent Keywords (from lead_service.py)
    LEAD_KEYWORDS = [
        "private event", "party", "birthday", "reservation", "book",
        "corporate", "holiday party", "large group", "catering",
        "wedding", "brunch", "fundraiser"
    ]


settings = Settings()