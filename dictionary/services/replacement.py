"""
Public, transform-only replacement service for final output boundaries.

This service is MCP-safe: it accepts only text, applies active dictionary
entries, performs no filtering, and does not write to the database.
"""

from dictionary.models import Entry
from dictionary.replacement import replace


def replace_text(text: str) -> str:
    """
    Replace internal identifiers using all active entries.

    This is the final replacement boundary. It accepts only text, performs no
    filtering, injects no entries, and is deterministic and side-effect free.
    """
    entries = Entry.objects.filter(is_active=True).iterator()
    return replace(text, entries=entries)
