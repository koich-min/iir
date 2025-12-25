"""
Internal orchestration service for human-controlled replacement workflows.

This service allows category filtering for CLI, Web UI, and API usage while
preserving the exact-match, deterministic replacement rules.
"""

from collections import defaultdict
from typing import Iterable

from django.db.models import QuerySet

from dictionary.models import Entry
from dictionary.replacement import pseudonym_for, replace, _sorted_replacements

def replace_text_internal(
    text: str,
    *,
    include_categories: Iterable[str] | None = None,
    exclude_categories: Iterable[str] | None = None,
) -> str:
    """
    Replace internal identifiers with optional category-based filtering.

    This is intended for CLI, Web UI, and API usage only. It performs no writes
    and delegates replacement to the core algorithm.
    """
    entries = _filtered_entries(include_categories, exclude_categories)
    if entries is None:
        return text
    return replace(text, entries=entries.iterator())


def replace_text_internal_with_counts(
    text: str,
    *,
    include_categories: Iterable[str] | None = None,
    exclude_categories: Iterable[str] | None = None,
) -> tuple[str, dict[str, int]]:
    """
    Replace internal identifiers and return per-category replacement counts.

    This helper is intended for CLI dry-run output and remains side-effect free.
    """
    entries = _filtered_entries(include_categories, exclude_categories)
    if entries is None:
        return text, {}

    entry_list = list(entries)
    if not entry_list:
        return text, {}

    replacements = _sorted_replacements(entry_list)
    category_map = {
        (entry.value, pseudonym_for(entry)): entry.category
        for entry in entry_list
    }

    counts: dict[str, int] = defaultdict(int)
    output = text
    for value, pseudonym in replacements:
        occurrences = output.count(value)
        if not occurrences:
            continue
        category = category_map.get((value, pseudonym))
        if category is not None:
            counts[category] += occurrences
        output = output.replace(value, pseudonym)

    return output, dict(counts)


def _filtered_entries(
    include_categories: Iterable[str] | None,
    exclude_categories: Iterable[str] | None,
) -> QuerySet[Entry] | None:
    entries = Entry.objects.filter(is_active=True)
    if include_categories is not None:
        include_list = list(include_categories)
        if not include_list:
            return None
        return entries.filter(category__in=include_list)
    if exclude_categories:
        return entries.exclude(category__in=exclude_categories)
    return entries
