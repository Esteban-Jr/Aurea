from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Booking

class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password123")

    def test_booking_form_renders(self):
        # login first, otherwise redirected (302)
        self.client.login(username="tester", password="password123")
        response = self.client.get(reverse("create_bookings"))
        self.assertEqual(response.status_code, 200)
        # match your actual template name
        self.assertTemplateUsed(response, "bookings/create_bookings.html")

    def test_create_booking(self):
        self.client.login(username="tester", password="password123")
        response = self.client.post(reverse("create_bookings"), {
            "name": "John Doe",
            "date": "2025-12-01",
            "time": "18:30",   # must match your ChoiceField format (string)
            "guests": 2,
            "phone_number": "7123456789",
            "email": "john@example.com",
        })
        # should redirect to booking_success on success
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("booking_success"))
        self.assertEqual(Booking.objects.count(), 1)