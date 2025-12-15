from datetime import date, timedelta

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
        self.assertTemplateUsed(response, "bookings/create_bookings.html")

    def test_create_booking(self):
        self.client.login(username="tester", password="password123")

        future_date = date.today() + timedelta(days=7)

        response = self.client.post(
            reverse("create_bookings"),
            {
                "name": "John Doe",
                "date": future_date.strftime("%Y-%m-%d"),
                "time": "18:30",
                "guests": 2,
                "phone_number": "7123456789",
                "email": "john@example.com",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("booking_success"))
        self.assertEqual(Booking.objects.count(), 1)

    def test_cannot_create_booking_in_past(self):
        self.client.login(username="tester", password="password123")

        past_date = date.today() - timedelta(days=1)

        response = self.client.post(
            reverse("create_bookings"),
            {
                "name": "John Doe",
                "date": past_date.strftime("%Y-%m-%d"),
                "time": "18:30",
                "guests": 2,
                "phone_number": "7123456789",
                "email": "john@example.com",
            },
        )

        # Invalid form should re-render with status 200 and not save anything
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
