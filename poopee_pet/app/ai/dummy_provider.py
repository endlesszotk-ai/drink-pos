import random

from .base import AIProvider

_REPLIES = [
    "เมี๊ยว~ ตอนนี้ยังไม่ได้ต่อ API นะ",
    "โปสตี้รับทราบ เดี๋ยวให้ต่อสมองให้ก่อนนะ",
    "แง่ว… ขอต่อ GEMINI_API_KEY ก่อน แล้วจะฉลาดขึ้น",
    "เข้าใจแล้วเมี๊ยว แต่ตอนนี้ยังเป็นโหมดทดลองอยู่",
    "ถามมาดีมากเลย แต่ขอ API key ก่อนนะจ๊ะ ~",
]


class DummyProvider(AIProvider):
    def ask(self, message: str) -> str:
        return random.choice(_REPLIES)
