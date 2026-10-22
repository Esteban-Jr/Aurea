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

    def test_past_date_error_is_translated(self):
        self.client.login(username="tester", password="password123")
        self.client.cookies["django_language"] = "es"
        past_date = date.today() - timedelta(days=1)
        response = self.client.post(
            reverse("create_bookings"),
            {
                "name": "Juan",
                "date": past_date.strftime("%Y-%m-%d"),
                "time": "18:30",
                "guests": 2,
                "phone_number": "7123456789",
                "email": "juan@example.com",
            },
        )
        self.assertContains(response, "No puedes reservar una fecha pasada.")

    def test_edit_form_keeps_iso_date_in_spanish(self):
        # <input type="date"> only understands 2026-10-22, not 22/10/2026
        self.client.login(username="tester", password="password123")
        self.client.cookies["django_language"] = "es"
        booking = Booking.objects.create(
            user=self.user, date=date.today() + timedelta(days=3), time="19:00",
            guests=2, name="Juan", email="juan@example.com", phone_number="7123456789",
        )
        response = self.client.get(reverse("edit_booking", args=[booking.pk]))
        self.assertContains(response, f'value="{booking.date.isoformat()}"')

    def test_booking_with_colombian_number(self):
        self.client.login(username="tester", password="password123")
        response = self.client.post(reverse("create_bookings"), {
            "name": "Ana", "date": (date.today() + timedelta(days=2)).isoformat(), "time": "20:00",
            "guests": 3, "phone_country": "CO", "phone_number": "3001234567", "email": "ana@example.com",
        })
        self.assertRedirects(response, reverse("booking_success"))
        booking = Booking.objects.get()
        self.assertEqual(booking.phone_number, "+573001234567")
        self.assertEqual(booking.full_phone(), "+573001234567")

    def test_old_uk_number_without_country_still_works(self):
        # the existing tests post only "7123456789": the picker defaults to the UK
        self.client.login(username="tester", password="password123")
        self.client.post(reverse("create_bookings"), {
            "name": "Ana", "date": (date.today() + timedelta(days=2)).isoformat(), "time": "20:00",
            "guests": 3, "phone_number": "7123456789", "email": "ana@example.com",
        })
        self.assertEqual(Booking.objects.get().phone_number, "+447123456789")


class StaffBookingTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("host", password="pass12345!", is_staff=True)
        self.guest = User.objects.create_user("guest", password="pass12345!")
        self.booking = Booking.objects.create(
            user=self.guest, date=date.today() + timedelta(days=1), time="19:00", guests=2,
            name="Laura Pérez", email="laura@example.com", phone_number="+573001234567",
        )
        Booking.objects.create(user=self.guest, date=date.today() - timedelta(days=3), time="13:00", guests=4,
                               name="Old Booking", email="old@example.com", phone_number="+447123456789")
        self.client.login(username="host", password="pass12345!")

    def test_list_shows_upcoming_by_default_and_past_on_request(self):
        response = self.client.get(reverse("staff_bookings"))
        self.assertContains(response, "Laura Pérez")
        self.assertNotContains(response, "Old Booking")
        self.assertContains(self.client.get(reverse("staff_bookings") + "?show=past"), "Old Booking")

    def test_search(self):
        response = self.client.get(reverse("staff_bookings") + "?show=all&q=laura")
        self.assertContains(response, "Laura Pérez")
        self.assertNotContains(response, "Old Booking")

    def test_staff_can_edit_someone_elses_booking(self):
        response = self.client.post(reverse("staff_booking_edit", args=[self.booking.pk]), {
            "name": "Laura Pérez", "date": self.booking.date.isoformat(), "time": "20:30", "guests": 6,
            "phone_country": "CO", "phone_number": "3001234567", "email": "laura@example.com",
        })
        self.assertRedirects(response, reverse("staff_bookings"))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.guests, 6)
        self.assertEqual(self.booking.user, self.guest)   # still the guest's booking

    def test_staff_can_cancel_a_booking(self):
        self.client.post(reverse("staff_booking_cancel", args=[self.booking.pk]))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())
