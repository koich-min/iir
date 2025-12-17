from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Entry
from .replacement import pseudonym_for, replace


class EntryModelTests(TestCase):
    def test_value_unique_within_category(self):
        Entry.objects.create(category="HOST", value="srv-prod-01")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Entry.objects.create(category="HOST", value="srv-prod-01")

        # Same value is allowed in a different category.
        Entry.objects.create(category="SERVICE", value="srv-prod-01")

    def test_pseudonym_requires_saved_entry(self):
        unsaved = Entry(category="HOST", value="unsaved")

        with self.assertRaises(ValueError):
            pseudonym_for(unsaved)


class ReplacementTests(TestCase):
    def test_inactive_entries_are_skipped(self):
        active = Entry.objects.create(category="HOST", value="active-host")
        Entry.objects.create(
            category="HOST", value="offline-host", is_active=False
        )

        result = replace("active-host offline-host")
        self.assertEqual(result, f"Host{active.id} offline-host")

    def test_replacements_apply_longest_value_first(self):
        long_entry = Entry.objects.create(category="HOST", value="srv-prod-01")
        short_entry = Entry.objects.create(category="HOST", value="srv")

        result = replace("srv-prod-01 srv srv-prod-01")

        self.assertEqual(
            result,
            f"Host{long_entry.id} Host{short_entry.id} Host{long_entry.id}",
        )

    def test_multiple_categories_are_replaced(self):
        host = Entry.objects.create(category="HOST", value="alpha")
        service = Entry.objects.create(category="SERVICE", value="bravo")

        result = replace("alpha bravo")

        self.assertEqual(result, f"Host{host.id} Service{service.id}")

    def test_empty_values_raise(self):
        entry = Entry.objects.create(category="WORD", value="")

        with self.assertRaises(ValueError):
            replace("anything", entries=[entry])
