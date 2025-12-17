from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import CategorySuggestion, Entry
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


class CategorySuggestionTests(TestCase):
    def test_name_is_unique(self):
        CategorySuggestion.objects.create(name="HOST")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CategorySuggestion.objects.create(name="HOST")

    def test_note_is_optional_and_active_default(self):
        suggestion = CategorySuggestion.objects.create(name="SERVICE", note="")

        self.assertTrue(suggestion.is_active)
        self.assertEqual(suggestion.note, "")


class ReplaceViewTests(TestCase):
    def setUp(self):
        self.url = reverse("replace")

    def test_get_sets_default_categories_and_empty_output(self):
        Entry.objects.create(category="HOST", value="alpha")
        Entry.objects.create(category="WORD", value="beta", is_active=False)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["selected_categories"]),
            {"HOST"},
        )
        self.assertEqual(list(response.context["categories"]), ["HOST"])
        self.assertEqual(response.context["output"], "")
        self.assertEqual(response.context["text"], "")

    def test_post_applies_selected_categories_only(self):
        host = Entry.objects.create(category="HOST", value="alpha")
        Entry.objects.create(category="NAME", value="bravo")
        Entry.objects.create(category="WORD", value="charlie", is_active=False)

        response = self.client.post(
            self.url, {"text": "alpha bravo", "categories": ["HOST"]}
        )

        self.assertContains(response, f"Host{host.id}")
        self.assertContains(response, "bravo")

    def test_get_with_no_entries_renders_without_categories(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["categories"]), [])
        self.assertEqual(set(response.context["selected_categories"]), set())
        self.assertEqual(response.context["output"], "")
