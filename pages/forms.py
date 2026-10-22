from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ALLERGENS, Category, Dish


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name_en", "name_es", "order"]
        widgets = {
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_es": forms.TextInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }


class DishForm(forms.ModelForm):
    # Shown as tick boxes, saved as "gluten milk"
    allergen_list = forms.MultipleChoiceField(
        label=_("Allergens"),
        choices=list(ALLERGENS.items()),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = ["category", "name", "description_en", "description_es", "story_en", "story_es",
                  "image", "image_url", "vegetarian", "vegan", "gluten_free",
                  "featured", "available", "order"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description_en": forms.TextInput(attrs={"class": "form-control"}),
            "description_es": forms.TextInput(attrs={"class": "form-control"}),
            "story_en": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "story_es": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://…"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["allergen_list"] = self.instance.allergen_codes

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("vegan"):
            cleaned["vegetarian"] = True     # vegan dishes are vegetarian too
        if not cleaned.get("image") and not cleaned.get("image_url"):
            self.add_error("image", _("Upload a photo or paste a photo link."))
        return cleaned

    def save(self, commit=True):
        self.instance.allergens = " ".join(self.cleaned_data.get("allergen_list", []))
        return super().save(commit)
