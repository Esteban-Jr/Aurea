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


class DishCardTests(TestCase):
    def test_menu_has_card_data_for_every_dish(self):
        import json
        response = self.client.get(reverse("menu"))
        data = json.loads(response.context["dish_data"] and json.dumps(response.context["dish_data"]))
        self.assertEqual(len(data), 30)
        risotto = data["risotto-al-tartufo"]
        self.assertIn("Vegetarian", risotto["tags"])
        self.assertIn("Milk", risotto["allergens"])
        self.assertContains(response, 'data-dish="risotto-al-tartufo"')
        self.assertContains(response, 'id="dish-data"')

    def test_card_text_is_spanish(self):
        self.client.cookies["django_language"] = "es"
        data = self.client.get(reverse("menu")).context["dish_data"]
        self.assertIn("Sin gluten", data["risotto-al-tartufo"]["tags"])
        self.assertTrue(data["risotto-al-tartufo"]["story"].startswith("Arroz arborio"))
        self.assertEqual(data["risotto-al-tartufo"]["name"], "Risotto al Tartufo")


class StaffMenuTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.staff = User.objects.create_user("chef", password="pass12345!", is_staff=True)
        self.customer = User.objects.create_user("guest", password="pass12345!")

    def dish_data(self, **extra):
        from .models import Category
        data = {"category": Category.objects.get(slug="mains").pk, "name": "Lasagne della Nonna",
                "description_en": "Layers of pasta, ragù and béchamel.", "description_es": "Capas de pasta, ragú y bechamel.",
                "image_url": "https://example.com/lasagne.jpg", "allergen_list": ["gluten", "milk"],
                "available": "on", "order": 9}
        data.update(extra)
        return data

    def test_staff_pages_are_staff_only(self):
        url = reverse("manage_menu")
        self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")
        self.client.login(username="guest", password="pass12345!")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.get(reverse("staff_bookings")).status_code, 403)
        self.client.login(username="chef", password="pass12345!")
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_staff_can_add_a_dish_and_it_shows_on_the_menu(self):
        from .models import Dish
        self.client.login(username="chef", password="pass12345!")
        response = self.client.post(reverse("dish_create"), self.dish_data())
        self.assertRedirects(response, reverse("manage_menu"))
        dish = Dish.objects.get(name="Lasagne della Nonna")
        self.assertEqual(dish.slug, "lasagne-della-nonna")
        self.assertEqual(dish.allergens, "gluten milk")
        self.assertContains(self.client.get(reverse("menu")), "Lasagne della Nonna")
        self.client.cookies["django_language"] = "es"
        self.assertContains(self.client.get(reverse("menu")), "Capas de pasta, ragú y bechamel.")

    def test_dish_needs_a_photo(self):
        self.client.login(username="chef", password="pass12345!")
        response = self.client.post(reverse("dish_create"), self.dish_data(image_url=""))
        self.assertContains(response, "Upload a photo or paste a photo link.")

    def test_staff_can_upload_a_photo(self):
        import io, shutil, tempfile
        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings
        from PIL import Image
        from .models import Dish
        buf = io.BytesIO(); Image.new("RGB", (8, 8), "gold").save(buf, "JPEG")
        media = tempfile.mkdtemp()
        try:
            with override_settings(MEDIA_ROOT=media, DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage"):
                self.client.login(username="chef", password="pass12345!")
                photo = SimpleUploadedFile("lasagne.jpg", buf.getvalue(), content_type="image/jpeg")
                self.client.post(reverse("dish_create"), self.dish_data(image_url="", image=photo))
                self.assertTrue(Dish.objects.get(name="Lasagne della Nonna").photo.endswith(".jpg"))
        finally:
            shutil.rmtree(media)

    def test_hide_and_show_a_dish(self):
        from .models import Dish
        self.client.login(username="chef", password="pass12345!")
        dish = Dish.objects.get(slug="risotto-al-tartufo")
        self.client.post(reverse("dish_toggle", args=[dish.pk]))
        self.assertNotContains(self.client.get(reverse("menu")), 'data-dish="risotto-al-tartufo"')
        self.client.post(reverse("dish_toggle", args=[dish.pk]))
        self.assertContains(self.client.get(reverse("menu")), 'data-dish="risotto-al-tartufo"')

    def test_edit_and_delete_a_dish(self):
        from .models import Dish
        self.client.login(username="chef", password="pass12345!")
        dish = Dish.objects.get(slug="torta-caprese")
        data = self.dish_data(name="Torta Caprese", category=dish.category.pk, description_en="Now with hazelnuts.",
                              image_url=dish.image_url)
        self.client.post(reverse("dish_edit", args=[dish.pk]), data)
        dish.refresh_from_db()
        self.assertEqual(dish.description_en, "Now with hazelnuts.")
        self.client.post(reverse("dish_delete", args=[dish.pk]))
        self.assertFalse(Dish.objects.filter(pk=dish.pk).exists())

    def test_category_with_dishes_cannot_be_deleted(self):
        from .models import Category
        self.client.login(username="chef", password="pass12345!")
        mains = Category.objects.get(slug="mains")
        self.client.post(reverse("category_delete", args=[mains.pk]))
        self.assertTrue(Category.objects.filter(pk=mains.pk).exists())

    def test_next_cannot_leave_the_site(self):
        from .models import Dish
        self.client.login(username="chef", password="pass12345!")
        dish = Dish.objects.get(slug="torta-caprese")
        data = self.dish_data(name="Torta Caprese", category=dish.category.pk, image_url=dish.image_url,
                              next="https://evil.example/")
        response = self.client.post(reverse("dish_edit", args=[dish.pk]), data)
        self.assertRedirects(response, reverse("manage_menu"))

    def test_profile_shows_staff_tools_only_to_staff(self):
        self.client.login(username="guest", password="pass12345!")
        self.assertNotContains(self.client.get(reverse("profile")), "Admin panel")
        self.client.login(username="chef", password="pass12345!")
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "Admin panel")
        self.assertContains(response, reverse("admin:index"))

    def test_admin_has_link_back_to_website(self):
        self.staff.is_superuser = True
        self.staff.save()
        self.client.login(username="chef", password="pass12345!")
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "Back to website")
        self.assertContains(response, "Dishes")
