from django.contrib import admin

from .models import Category, Dish


class DishInline(admin.TabularInline):
    model = Dish
    fields = ("name", "description_en", "available", "featured", "order")
    extra = 0
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_es", "order")
    list_editable = ("order",)
    inlines = [DishInline]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "available", "featured", "vegetarian", "vegan", "gluten_free", "order")
    list_editable = ("available", "featured", "order")
    list_filter = ("category", "available", "featured", "vegetarian", "vegan", "gluten_free")
    search_fields = ("name", "description_en", "description_es")
    prepopulated_fields = {"slug": ("name",)}
