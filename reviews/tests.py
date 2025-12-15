from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Review


class ReviewTests(TestCase):
    def setUp(self):
        self.password = "password123"
        self.user = User.objects.create_user(
            username="tester",
            password=self.password,
            email="tester@example.com",
        )

    def test_review_list_renders(self):
        response = self.client.get(reverse("review_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_list.html")

    def test_add_review_requires_login_edge_case(self):
        response = self.client.get(reverse("add_review"))
        # login_required should redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_review(self):
        self.client.login(username="tester", password=self.password)

        response = self.client.post(
            reverse("add_review"),
            {
                "comment": "Great food and great service!",
                "rating": 5,  # model expects an int 1-5
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("review_list"))
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user, self.user)

    def test_user_can_edit_own_review(self):
        self.client.login(username="tester", password=self.password)
        review = Review.objects.create(user=self.user, comment="Okay", rating=3, approved=True)

        response = self.client.post(
            reverse("edit_review", args=[review.pk]),
            {"comment": "Actually, it was excellent!", "rating": 5},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("review_list"))
        review.refresh_from_db()
        self.assertEqual(review.comment, "Actually, it was excellent!")
        self.assertEqual(review.rating, 5)

    def test_user_can_delete_own_review(self):
        self.client.login(username="tester", password=self.password)
        review = Review.objects.create(user=self.user, comment="Will delete", rating=2, approved=True)

        response = self.client.post(reverse("delete_review", args=[review.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("review_list"))
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())
