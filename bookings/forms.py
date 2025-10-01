from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, DateInput, NumberInput, Textarea
from datetime import datetime, date
from .models import Booking

# Every 30 minutes between 09:00–21:00
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
                'placeholder': 'Any special requests?'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t_str = cleaned.get("time")

        if d:
            today = date.today()
            now = datetime.now().time()

            # Editing: prevent editing past bookings
            if self.instance and self.instance.pk and self.instance.date < today:
                raise ValidationError("Past bookings cannot be edited.")

            # Prevent selecting past dates
            if d < today:
                raise ValidationError("You cannot book a date in the past.")

            # Prevent past times for today
            if d == today and t_str:
                t = datetime.strptime(t_str, "%H:%M").time()
                if t <= now:
                    raise ValidationError("You cannot book a time that has already passed today.")

        # Prevent double booking
        if self.user and d and t_str:
            t = datetime.strptime(t_str, "%H:%M").time()  # convert string to time
            exists = Booking.objects.filter(
                user=self.user, date=d, time=t
            ).exclude(id=self.instance.id if self.instance else None).exists()
            if exists:
                raise ValidationError("You already have a booking at this time.")

        return cleaned