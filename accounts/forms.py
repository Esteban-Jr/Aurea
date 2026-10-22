from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from . import phone


class PhoneMixin:
    """Adds 'phone_country' + 'phone_number'; clean() leaves the full number in cleaned_data['phone']."""

    def clean(self):
        cleaned = super().clean()
        number = (cleaned.get("phone_number") or "").strip()
        cleaned["phone"] = ""
        if number:
            try:
                cleaned["phone"] = phone.to_e164(cleaned.get("phone_country"), number)
            except forms.ValidationError as error:
                self.add_error("phone_number", error)
        return cleaned


class SignUpForm(PhoneMixin, UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,
                                label=_("First name"), help_text=_("Enter your first name"))
    last_name = forms.CharField(max_length=30, required=True,
                                label=_("Last name"), help_text=_("Enter your last name"))
    email = forms.EmailField(required=True, label=_("Email"))
    phone_country = phone.country_field(required=False)
    phone_number = phone.number_field(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                'email', 'password1', 'password2')


class UserUpdateForm(PhoneMixin, forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_country = phone.country_field(required=False)
    phone_number = phone.number_field(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = getattr(self.instance, "profile", None)
        if profile and profile.phone and not self.is_bound:
            self.initial["phone_country"], self.initial["phone_number"] = phone.split(profile.phone)
