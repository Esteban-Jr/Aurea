"""International phone numbers: a country prefix picker plus a number box.

Numbers are checked with the `phonenumbers` library (Google's rules for every
country) and stored in E.164 format, e.g. "+573001234567".
"""
import unicodedata

import phonenumbers
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from .countries import NAMES

DEFAULT_COUNTRY = "GB"
POPULAR = ["GB", "CO", "ES", "US", "MX", "IT"]   # shown first in the list


def flag(region):
    """'CO' -> 🇨🇴 (two regional-indicator letters)."""
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in region)


def dial_code(region):
    return f"+{phonenumbers.country_code_for_region(region)}"


def example(region):
    """A sample local number for the placeholder, e.g. '321 1234567' for Colombia."""
    number = (phonenumbers.example_number_for_type(region, phonenumbers.PhoneNumberType.MOBILE)
              or phonenumbers.example_number(region))
    if not number:
        return ""
    text = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return text.replace(dial_code(region), "", 1).strip()


def country_name(region):
    english, spanish = NAMES[region]
    return spanish if (get_language() or "en").startswith("es") else english


def country_choices():
    """Grouped choices in the visitor's language: popular countries, then A–Z."""
    def label(region):
        return f"{flag(region)} {country_name(region)} ({dial_code(region)})"

    def sort_key(region):  # sort "Österreich" next to "Oman", not after "Z"
        return unicodedata.normalize("NFD", country_name(region)).encode("ascii", "ignore").lower()

    everyone = sorted(NAMES, key=sort_key)
    return [
        (_("Popular"), [(r, label(r)) for r in POPULAR]),
        (_("All countries"), [(r, label(r)) for r in everyone]),
    ]


class CountrySelect(forms.Select):
    """A <select> whose options carry their prefix and a sample number for the script."""

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option["attrs"]["data-dial"] = dial_code(value)
            option["attrs"]["data-example"] = example(value)
        return option


def country_field(required=True):
    return forms.ChoiceField(
        label=gettext_lazy("Country"),
        choices=country_choices,            # callable: rebuilt per form, so it follows the language
        initial=DEFAULT_COUNTRY,
        required=required,
        widget=CountrySelect(attrs={"class": "form-select phone-country"}),
    )


def number_field(required=True):
    return forms.CharField(
        label=gettext_lazy("Phone number"),
        max_length=30,
        required=required,
        widget=forms.TextInput(attrs={
            "class": "form-control phone-number",
            "type": "tel",
            "autocomplete": "tel-national",
            "inputmode": "tel",
        }),
    )


def to_e164(region, number):
    """Check a number for a country and return it as '+573001234567'."""
    region = region or DEFAULT_COUNTRY
    try:
        parsed = phonenumbers.parse(number, region)
    except phonenumbers.NumberParseException:
        parsed = None
    if parsed is None or not phonenumbers.is_valid_number(parsed):
        raise ValidationError(
            _("Enter a valid phone number for %(country)s (%(code)s).")
            % {"country": country_name(region), "code": dial_code(region)},
            code="invalid_phone",
        )
    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)


def split(e164):
    """'+573001234567' -> ('CO', '3001234567'), for filling in the form again."""
    if not e164:
        return DEFAULT_COUNTRY, ""
    try:
        parsed = phonenumbers.parse(e164, None if e164.startswith("+") else DEFAULT_COUNTRY)
    except phonenumbers.NumberParseException:
        return DEFAULT_COUNTRY, e164
    region = phonenumbers.region_code_for_number(parsed)
    if region not in NAMES:
        region = DEFAULT_COUNTRY
    return region, phonenumbers.national_significant_number(parsed)


def pretty(e164):
    """'+573001234567' -> '+57 300 1234567' for showing on the profile."""
    try:
        return phonenumbers.format_number(phonenumbers.parse(e164, None),
                                          phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        return e164
