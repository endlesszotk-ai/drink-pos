import os
from pathlib import Path

from .base import AIProvider
from .dummy_provider import DummyProvider
from .gemini_provider import GeminiProvider

__all__ = ["AIProvider", "DummyProvider", "GeminiProvider", "get_provider"]


def get_provider(root: Path) -> AIProvider:
    try:
        from dotenv import load_dotenv
        load_dotenv(root / ".env")
    except ImportError:
        pass

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        try:
            return GeminiProvider(api_key)
        except Exception as exc:
            print(f"Gemini init failed, using DummyProvider: {exc}")
    return DummyProvider()
