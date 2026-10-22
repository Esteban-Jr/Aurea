"""Manage menu: staff add, edit, hide and delete dishes and categories from the website."""
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from aurea_project.staff import redirect_back, staff_required

from .forms import CategoryForm, DishForm
from .models import Category, Dish


@staff_required
def manage_menu(request):
    categories = Category.objects.prefetch_related("dishes")
    return render(request, "staff/menu_manage.html", {"categories": categories})


@staff_required
def dish_form(request, pk=None):
    dish = get_object_or_404(Dish, pk=pk) if pk else None
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            dish = form.save()
            messages.success(request, _("“%(name)s” was saved.") % {"name": dish.name})
            return redirect_back(request, "manage_menu")
    else:
        initial = {}
        if not dish and request.GET.get("category"):
            initial["category"] = request.GET["category"]
        form = DishForm(instance=dish, initial=initial)
    return render(request, "staff/dish_form.html", {"form": form, "dish": dish,
                                                    "next": request.GET.get("next", "")})


@staff_required
def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == "POST":
        dish.delete()
        messages.warning(request, _("“%(name)s” was removed from the menu.") % {"name": dish.name})
        return redirect("manage_menu")
    return render(request, "staff/confirm_delete.html", {
        "title": _("Delete dish"),
        "question": _("Delete “%(name)s” from the menu? This can’t be undone. "
                      "To hide it for a while instead, untick “Available”.") % {"name": dish.name},
        "cancel_url": "manage_menu",
    })


@staff_required
def dish_toggle(request, pk):
    """Quick show/hide button on the Manage menu page."""
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == "POST":
        dish.available = not dish.available
        dish.save(update_fields=["available"])
    return redirect("manage_menu")


@staff_required
def category_form(request, pk=None):
    category = get_object_or_404(Category, pk=pk) if pk else None
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        category = form.save()
        messages.success(request, _("“%(name)s” was saved.") % {"name": category.name})
        return redirect("manage_menu")
    return render(request, "staff/category_form.html", {"form": form, "category": category})


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        try:
            category.delete()
        except ProtectedError:
            messages.error(request, _("Move or delete the dishes in “%(name)s” first.") % {"name": category.name})
        else:
            messages.warning(request, _("“%(name)s” was deleted.") % {"name": category.name})
        return redirect("manage_menu")
    return render(request, "staff/confirm_delete.html", {
        "title": _("Delete category"),
        "question": _("Delete the category “%(name)s”?") % {"name": category.name},
        "cancel_url": "manage_menu",
    })
