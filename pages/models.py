"""The menu, editable by staff from the website (Manage menu) or the admin panel.

Dish names stay in Italian. Descriptions are typed in English and Spanish;
if the Spanish box is empty, the English text is shown instead.
"""
from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

# Dietary tags and the 14 UK allergens (labels are translated in locale/es)
TAGS = {"vegetarian": _("Vegetarian"), "vegan": _("Vegan"), "gluten_free": _("Gluten-free")}
ALLERGENS = {
    "gluten": _("Gluten"), "crustaceans": _("Crustaceans"), "eggs": _("Eggs"), "fish": _("Fish"),
    "peanuts": _("Peanuts"), "soya": _("Soya"), "milk": _("Milk"), "nuts": _("Nuts"),
    "celery": _("Celery"), "mustard": _("Mustard"), "sesame": _("Sesame"), "sulphites": _("Sulphites"),
    "lupin": _("Lupin"), "molluscs": _("Molluscs"),
}


def pick(english, spanish):
    """The Spanish text for Spanish visitors when there is one, otherwise the English."""
    if spanish and (get_language() or "en").startswith("es"):
        return spanish
    return english


def unique_slug(instance, text):
    base = slugify(text) or "item"
    slug, n = base, 2
    while type(instance).objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


class Category(models.Model):
    name_en = models.CharField(_("name (English)"), max_length=60)
    name_es = models.CharField(_("name (Spanish)"), max_length=60, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveSmallIntegerField(_("order"), default=0, help_text=_("Lower numbers come first."))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("menu category")
        verbose_name_plural = _("menu categories")

    def __str__(self):
        return self.name_en

    @property
    def name(self):
        return pick(self.name_en, self.name_es)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name_en)
        super().save(*args, **kwargs)


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="dishes",
                                 verbose_name=_("category"))
    name = models.CharField(_("name"), max_length=80, help_text=_("Usually the Italian name; it is not translated."))
    slug = models.SlugField(unique=True, blank=True)
    description_en = models.CharField(_("short description (English)"), max_length=200)
    description_es = models.CharField(_("short description (Spanish)"), max_length=200, blank=True)
    story_en = models.TextField(_("longer description (English)"), blank=True)
    story_es = models.TextField(_("longer description (Spanish)"), blank=True)
    image = models.ImageField(_("photo"), upload_to="dishes/", blank=True)
    image_url = models.URLField(_("or photo link"), max_length=500, blank=True,
                                help_text=_("Used when no photo is uploaded."))
    vegetarian = models.BooleanField(_("vegetarian"), default=False)
    vegan = models.BooleanField(_("vegan"), default=False)
    gluten_free = models.BooleanField(_("gluten-free"), default=False)
    allergens = models.CharField(_("allergens"), max_length=200, blank=True,
                                 help_text=_("Allergen codes separated by spaces, e.g. 'gluten milk'."))
    featured = models.BooleanField(_("featured on the home page"), default=False)
    available = models.BooleanField(_("available"), default=True,
                                    help_text=_("Untick to hide the dish without deleting it."))
    order = models.PositiveSmallIntegerField(_("order"), default=0, help_text=_("Lower numbers come first."))

    class Meta:
        ordering = ["category__order", "order", "id"]
        verbose_name = _("dish")
        verbose_name_plural = _("dishes")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)

    # What the templates show, in the visitor's language
    @property
    def description(self):
        return pick(self.description_en, self.description_es)

    @property
    def story(self):
        return pick(self.story_en, self.story_es)

    @property
    def photo(self):
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def allergen_codes(self):
        return [code for code in self.allergens.split() if code in ALLERGENS]

    @property
    def tags(self):
        return [str(label) for field, label in TAGS.items() if getattr(self, field)]

    @property
    def allergen_labels(self):
        return [str(ALLERGENS[code]) for code in self.allergen_codes]
