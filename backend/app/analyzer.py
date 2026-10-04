import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

MODEL = "gemma-4-26b-a4b-it"


def ask_gemma(question: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
    )

    return response.text


def analyze_repository(context: str) -> str:
    prompt = f"""
You are CONTribute, an AI assistant that helps developers
understand unfamiliar open-source repositories and make their
first contribution.

Analyze the repository context below.

Your response must cover:

1. What this repository does
2. Main architecture and important components
3. How a new contributor should understand the codebase
4. Important files to inspect first
5. How to run the project locally
6. Three realistic beginner-friendly contribution opportunities

Rules:
- Only use information present in the provided context.
- Do not invent files, technologies, commands, issues, or behavior.
- If something cannot be determined, explicitly say so.
- Be practical and concise.

REPOSITORY CONTEXT:

{context}
"""

    return ask_gemma(prompt)