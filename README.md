# ParksideAI

AI-powered SEO & hospitality assistant for Parkside Tavern in Morristown, NJ.

## Core Principles

- **Never** takes reservations directly
- **Never** collects guest personal information
- **Never** stores guest data
- Always routes to official links:
  - Reservations → OpenTable
  - Private Events → Tripleseat
  - General info → parksidenj.com

## Tech Stack

- Flask (Python)
- OpenAI API (gpt-4o-mini)
- Flask-Limiter for rate limiting
- SQLite for anonymous analytics
- Gunicorn for production

## Local Development

```bash
# Clone and install
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run
python run.py
