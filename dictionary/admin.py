from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "value", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("value", "category")
