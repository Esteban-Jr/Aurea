from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # International format, e.g. +447123456789 or +573001234567 (checked in BookingForm)
    phone_number = models.CharField(max_length=20)

    def full_phone(self):
        """The phone number with its country prefix (older bookings were UK-only)."""
        return self.phone_number if self.phone_number.startswith("+") else f"+44{self.phone_number}"

    def pretty_phone(self):
        """'+573001234567' -> '+57 300 1234567'."""
        from accounts.phone import pretty
        return pretty(self.full_phone())

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"