from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from django.forms import TextInput, DateInput, NumberInput, Textarea
from datetime import time, datetime

# Generate choices: every 30 minutes between 09:00 and 21:00
TIME_CHOICES = [(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(9, 22) for m in (0, 30)]

class BookingForm(forms.ModelForm):
    time = forms.ChoiceField(choices=TIME_CHOICES)

    class Meta:
        model = Booking
        fields = ['name', 'date', 'time',
                  'guests', 'phone_number', 'email', 'special_requests']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Your full name'}),
            'date': DateInput(attrs={'type': 'date'}),
            'guests': NumberInput(attrs={'min': 1, 'max': 25}),
            'phone_number': TextInput(attrs={'placeholder': '7123456789'}),
            'special_requests': Textarea(attrs={'rows': 3}),
        }

    def clean_time(self):
        t_str = self.cleaned_data['time']  # string like "18:30"
        t = datetime.strptime(t_str, "%H:%M").time()
        if t.minute not in (0, 30):
            raise ValidationError("Please choose a time in 30-minute intervals (e.g., 10:00, 10:30).")
        return t