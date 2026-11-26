from __future__ import annotations

from datetime import datetime, timezone


def utc_time() -> str:
    """A read-only example tool safe for local demonstrations."""
    return datetime.now(timezone.utc).isoformat()


def word_count(text: str) -> dict[str, int]:
    """Return deterministic text statistics without external side effects."""
    return {"words": len(text.split()), "characters": len(text)}
