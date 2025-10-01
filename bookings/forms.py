from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from django.forms import TextInput, DateInput, NumberInput, Textarea
from datetime import datetime

# Generate choices: every 30 minutes between 09:00 and 21:00
TIME_CHOICES = [(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(9, 22) for m in (0, 30)]

class BookingForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['name', 'date', 'time', 'guests', 'phone_number', 'email', 'special_requests']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'guests': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 25}),
            'phone_number': TextInput(attrs={'class': 'form-control', 'placeholder': '7123456789'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'special_requests': Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any special requests? (e.g. allergies, celebrations, seating preference)'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date:
            today = date.today()
            now = datetime.now().time()

            # Block editing of past bookings entirely
            if self.instance and self.instance.pk:
                if self.instance.date < today:
                    raise ValidationError("Past bookings cannot be edited.")

            # Block selecting a past date
            if date < today:
                raise ValidationError("You cannot book a date in the past.")

            # Block selecting a past time on the same day
            if date == today and time:
                t = datetime.strptime(time, "%H:%M").time()
                if t <= now:
                    raise ValidationError("You cannot book a time that has already passed today.")

        return cleaned_data
