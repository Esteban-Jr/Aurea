from django.test import TestCase
from django.urls import reverse

class PagesTests(TestCase):
    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")
