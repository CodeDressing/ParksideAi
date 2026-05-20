import os
from dotenv import load_dotenv
from openai import OpenAI

from parkside_chatbot.prompts import PARKSIDE_SYSTEM_PROMPT

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def generate_chat_response(user_message):
    if not user_message.strip():
        return "Please send me a message so I can help."

    if not api_key:
        return "OpenAI API key is missing. Please check your .env file."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": PARKSIDE_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as error:
        print("OPENAI ERROR:", error)
        return f"AI connection error: {str(error)}"