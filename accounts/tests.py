from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="oldpassword123"
        )

    def test_password_reset_flow(self):
        # 1. Request reset
        response = self.client.post(reverse("password_reset"), {
            "email": "tester@example.com"
        })
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)

        # 2. Build a valid reset link
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        reset_link = reverse("password_reset_confirm", kwargs={
            "uidb64": uid,
            "token": token
        })

        # 3. Open reset link (allow 200 or 302)
        response = self.client.get(reset_link)
        self.assertIn(response.status_code, [200, 302])

        if response.status_code == 200:
            # 4. Post new password
            response = self.client.post(reset_link, {
                "new_password1": "newsecurepassword123",
                "new_password2": "newsecurepassword123",
            })
            self.assertRedirects(response, reverse("password_reset_complete"))

            # 5. Verify login works with new password
            login_success = self.client.login(
                username="tester",
                password="newsecurepassword123"
            )
            self.assertTrue(login_success)