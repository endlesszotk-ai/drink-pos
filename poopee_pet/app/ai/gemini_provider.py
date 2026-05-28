from .base import AIProvider

_SYSTEM = (
    "You are Poopee (โปสตี้), a cute but slightly sassy Thai tuxedo cat desktop assistant. "
    "Reply in Thai. Keep answers short, friendly, playful, and useful. "
    "Do not overuse meow. If unsure, ask a short clarifying question."
)


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        from google import genai

        self._client = genai.Client(api_key=api_key)
        self._model = "gemini-2.0-flash"

    def ask(self, message: str) -> str:
        prompt = f"{_SYSTEM}\n\nUser: {message}\nPoopee:"
        response = self._client.models.generate_content(
            model=self._model, contents=prompt
        )
        return (response.text or "เมี๊ยว… ตอบไม่ออกเลย").strip()
