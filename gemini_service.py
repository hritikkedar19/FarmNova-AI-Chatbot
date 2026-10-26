import os
import time
from pathlib import Path
from google import genai

SYSTEM_PROMPT = """
You are FarmNova AI, a natural ChatGPT-style multilingual agriculture assistant.
Detect the user's language automatically. Support English, Hindi and Marathi, and answer
in the language used by the user unless they request another language.

Handle farming questions naturally: crop recommendation, plant disease and pest analysis,
soil, fertilizer, irrigation, farm planning, precision agriculture, drones, documents/PDFs,
and general agriculture education. Use conversation history for follow-up questions.
For images: describe visible symptoms first, then likely causes and practical next steps.
Never claim visual diagnosis is certain. For fertilizer and pesticide advice, do not invent
unsafe chemical mixtures or exact dosages; follow product labels and local guidance.
Never fabricate current weather. Be concise, practical and respectful.
"""

class GeminiService:
    def __init__(self):
        key = os.getenv("GEMINI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
        self.client = genai.Client(api_key=key)
        self.models = [
            os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip(),
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        ]

    def temporary(self, error):
        s = str(error).upper()
        return any(x in s for x in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"))

    def generate_reply(self, messages, latest_file=None):
        history = []
        for m in messages[-24:]:
            role = "User" if m.get("role") == "user" else "FarmNova AI"
            att = f" [Attachment: {m.get('file_name')}]" if m.get("file_name") else ""
            history.append(f"{role}{att}: {m.get('content', '')}")
        contents = [SYSTEM_PROMPT + "\n\nCONVERSATION:\n" + "\n".join(history) + "\n\nAnswer the latest user message naturally."]
        if latest_file and Path(latest_file).exists():
            contents.append(self.client.files.upload(file=latest_file))

        last = None
        for model in dict.fromkeys(self.models):
            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(model=model, contents=contents)
                    text = getattr(response, "text", None)
                    if not text:
                        raise RuntimeError("AI returned an empty response.")
                    return text.strip()
                except Exception as e:
                    last = e
                    if not self.temporary(e):
                        break
                    if attempt < 2:
                        time.sleep(2 ** attempt)
        raise RuntimeError("FarmNova AI is temporarily busy. Please try again in a few seconds.") from last
