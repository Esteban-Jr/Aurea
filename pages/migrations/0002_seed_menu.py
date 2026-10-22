"""Copy the menu that used to live in pages/content.py into the database."""
import json
from pathlib import Path

from django.db import migrations

SEED = Path(__file__).with_name("menu_seed.json")


def load_menu(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    Dish = apps.get_model("pages", "Dish")
    if Category.objects.exists():
        return
    for cat in json.loads(SEED.read_text(encoding="utf-8")):
        dishes = cat.pop("dishes")
        category = Category.objects.create(**cat)
        for dish in dishes:
            Dish.objects.create(category=category, **dish)


def remove_menu(apps, schema_editor):
    apps.get_model("pages", "Dish").objects.all().delete()
    apps.get_model("pages", "Category").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_menu, remove_menu),
    ]
