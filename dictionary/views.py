from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Entry
from .replacement import replace


CATEGORIES = ["HOST", "NAME", "SERVICE", "WORD"]


@require_http_methods(["GET", "POST"])
def replace_view(request):
    selected = set(request.POST.getlist("categories")) if request.method == "POST" else set(CATEGORIES)
    text = request.POST.get("text", "") if request.method == "POST" else ""
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
        "categories": CATEGORIES,
        "selected_categories": selected,
        "text": text,
        "output": output,
    }
    return render(request, "dictionary/replace.html", context)
