from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import CategorySuggestion, Entry
from .replacement import replace


@require_http_methods(["GET", "POST"])
def replace_view(request):
    categories = list(
        Entry.objects.filter(is_active=True)
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    if request.method == "POST":
        selected = set(request.POST.getlist("categories"))
        text = request.POST.get("text", "")
    else:
        selected = set(categories)
        text = ""
    output = ""

    if request.method == "POST":
        try:
            if selected:
                entries = Entry.objects.filter(
                    is_active=True, category__in=selected
                ).iterator()
                output = replace(text, entries=entries)
            else:
                output = text
        except Exception:
            output = text

    context = {
        "categories": categories,
        "selected_categories": selected,
        "text": text,
        "output": output,
        "category_suggestions": CategorySuggestion.objects.filter(
            is_active=True
        ),
    }
    return render(request, "dictionary/replace.html", context)
