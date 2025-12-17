from django.contrib import admin

from .models import CategorySuggestion, Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("category", "value", "is_active")
    list_filter = ("category", "is_active")


@admin.register(CategorySuggestion)
class CategorySuggestionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
