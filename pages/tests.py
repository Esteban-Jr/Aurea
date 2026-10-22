from django.test import TestCase
from django.urls import reverse


class PagesTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_about_page_renders(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")

    def test_menu_page_renders(self):
        response = self.client.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/menu.html")

    def test_faq_page_renders(self):
        response = self.client.get(reverse("faq"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/faq.html")

    def test_gallery_page_renders(self):
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/gallery.html")

    def test_invalid_page_returns_404_edge_case(self):
        response = self.client.get("/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)


class LanguageTests(TestCase):
    """English by default, Spanish when the visitor picks ES (cookie)."""

    def use_spanish(self):
        self.client.cookies["django_language"] = "es"

    def test_english_is_default(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, "Book a table")

    def test_spanish_when_cookie_set(self):
        self.use_spanish()
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<html lang="es">')
        self.assertContains(response, "Reservar mesa")
        self.assertNotContains(response, "Book a table")

    def test_menu_keeps_italian_names_and_translates_descriptions(self):
        self.use_spanish()
        response = self.client.get(reverse("menu"))
        self.assertContains(response, "Bruschetta Classica")
        self.assertContains(response, "Pan rústico tostado")

    def test_switch_sets_cookie_and_returns_to_same_page(self):
        response = self.client.post(reverse("set_language"), {"language": "es", "next": reverse("menu")})
        self.assertRedirects(response, reverse("menu"), fetch_redirect_response=False)
        self.assertEqual(response.cookies["django_language"].value, "es")
        self.assertContains(self.client.get(reverse("menu")), "Nuestra carta")

    def test_switch_ignores_outside_next_url(self):
        response = self.client.post(reverse("set_language"), {"language": "es", "next": "https://evil.example/"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")

    def test_every_page_renders_in_both_languages(self):
        for lang in ("en", "es"):
            self.client.cookies["django_language"] = lang
            for name in ("home", "about", "menu", "faq", "gallery", "review_list", "login", "signup"):
                with self.subTest(lang=lang, page=name):
                    self.assertEqual(self.client.get(reverse(name)).status_code, 200)
