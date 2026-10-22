from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, 
                                label=_("First name"), help_text=_("Enter your first name"))
    last_name = forms.CharField(max_length=30, required=True,
                                label=_("Last name"), help_text=_("Enter your last name"))
    email = forms.EmailField(required=True, label=_("Email"))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
