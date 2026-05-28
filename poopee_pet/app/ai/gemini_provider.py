import json
import urllib.request

from .base import AIProvider

_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key={key}"
)

_SYSTEM = (
    "You are Poopee (โปสตี้), a cute but slightly sassy Thai tuxedo cat desktop assistant. "
    "Reply in Thai. Keep answers short, friendly, playful, and useful. "
    "Do not overuse meow. If unsure, ask a short clarifying question."
)


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._sdk_client = None
        # Try to load the SDK for richer future use; fall back to REST if unavailable
        try:
            from google import genai
            self._sdk_client = genai.Client(api_key=api_key)
        except Exception:
            pass  # will use urllib REST path

    def ask(self, message: str) -> str:
        if self._sdk_client is not None:
            return self._ask_sdk(message)
        return self._ask_rest(message)

    # ── SDK path (google-genai installed) ─────────────────────────────────────

    def _ask_sdk(self, message: str) -> str:
        prompt = f"{_SYSTEM}\n\nUser: {message}\nPoopee:"
        response = self._sdk_client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return (response.text or "เมี๊ยว… ตอบไม่ออกเลย").strip()

    # ── REST path (stdlib only) ────────────────────────────────────────────────

    def _ask_rest(self, message: str) -> str:
        url = _API_URL.format(key=self._api_key)
        payload = {
            "system_instruction": {"parts": [{"text": _SYSTEM}]},
            "contents": [{"parts": [{"text": message}]}],
            "generationConfig": {"maxOutputTokens": 256, "temperature": 0.8},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read())
        text = body["candidates"][0]["content"]["parts"][0]["text"]
        return (text or "เมี๊ยว… ตอบไม่ออกเลย").strip()
