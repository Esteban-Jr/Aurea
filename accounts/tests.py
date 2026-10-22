from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):
    def setUp(self):
        self.password = "password123"
        self.user = User.objects.create_user(
            username="tester",
            password=self.password,
            email="tester@example.com",
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        if response.status_code == 200:
            print(response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "tester", "password": self.password},
        )
        # Successful login should redirect somewhere (often LOGIN_REDIRECT_URL)
        self.assertEqual(response.status_code, 302)

        # Confirm the user is actually authenticated by accessing a protected page
        protected = self.client.get(reverse("profile"))
        self.assertEqual(protected.status_code, 200)

    def test_login_fails_with_invalid_password_edge_case(self):
        response = self.client.post(
            reverse("login"),
            {"username": "tester", "password": "wrongpassword"},
        )
        # Django LoginView re-renders the form with errors on failure (200)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Still blocked from protected page
        protected = self.client.get(reverse("profile"))
        self.assertEqual(protected.status_code, 302)

    def test_logout_requires_post_and_logs_user_out(self):
        # log in first
        self.client.login(username="tester", password=self.password)

        # Your logout_confirm logs out only on POST
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)

        # Confirm user is logged out by checking protected page redirects
        protected = self.client.get(reverse("profile"))
        self.assertEqual(protected.status_code, 302)


class PhoneTests(TestCase):
    def signup(self, **extra):
        data = {
            "username": "maria", "email": "maria@example.com", "first_name": "María", "last_name": "Gómez",
            "password1": "StrongPass123!", "password2": "StrongPass123!",
        }
        data.update(extra)
        return self.client.post(reverse("signup"), data)

    def test_signup_with_colombian_number(self):
        response = self.signup(phone_country="CO", phone_number="300 123 4567")
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(User.objects.get(username="maria").profile.phone, "+573001234567")

    def test_signup_without_number_is_fine(self):
        self.assertRedirects(self.signup(), reverse("login"))
        self.assertEqual(User.objects.get(username="maria").profile.phone, "")

    def test_wrong_number_for_country_is_rejected(self):
        response = self.signup(phone_country="CO", phone_number="12345")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid phone number for Colombia (+57).")
        self.assertFalse(User.objects.filter(username="maria").exists())

    def test_prefix_options_carry_dial_codes(self):
        response = self.client.get(reverse("signup"))
        self.assertContains(response, 'data-dial="+57"')
        self.assertContains(response, "Colombia (+57)")

    def test_country_names_follow_language(self):
        self.client.cookies["django_language"] = "es"
        self.assertContains(self.client.get(reverse("signup")), "Reino Unido (+44)")

    def test_booking_form_is_prefilled_from_profile(self):
        self.signup(phone_country="CO", phone_number="3001234567")
        self.client.login(username="maria", password="StrongPass123!")
        form = self.client.get(reverse("create_bookings")).context["form"]
        self.assertEqual(form.initial["phone_country"], "CO")
        self.assertEqual(form.initial["phone_number"], "3001234567")
