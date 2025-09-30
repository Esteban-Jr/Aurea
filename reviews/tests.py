from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review

class ReviewTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="tester", password="password123")

    def test_review_list_page_renders(self):
        """Review list page should load and return 200"""
        response = self.client.get(reverse("review_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_list.html")

    def test_add_review_requires_login(self):
        """Anonymous users should be redirected when trying to add a review"""
        response = self.client.get(reverse("add_review"))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_logged_in_user_can_add_review(self):
        """Logged-in users should be able to add a review"""
        self.client.login(username="tester", password="password123")
        response = self.client.post(reverse("add_review"), {
            "rating": 5,
            "comment": "Amazing food and service!"
        })
        # Should redirect back to review_list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().comment, "Amazing food and service!")

    def test_logged_in_user_can_edit_own_review(self):
        """Logged-in users should be able to edit their own review"""
        self.client.login(username="tester", password="password123")
        review = Review.objects.create(user=self.user, rating=4, comment="Good service")
        
        response = self.client.post(reverse("edit_review", args=[review.id]), {
            "rating": 5,
            "comment": "Excellent service!"
        })
        self.assertEqual(response.status_code, 302)  # redirect after save
        review.refresh_from_db()
        self.assertEqual(review.comment, "Excellent service!")
        self.assertEqual(review.rating, 5)

    def test_logged_in_user_can_delete_own_review(self):
        """Logged-in users should be able to delete their own review"""
        self.client.login(username="tester", password="password123")
        review = Review.objects.create(user=self.user, rating=3, comment="Okay experience")
        
        response = self.client.post(reverse("delete_review", args=[review.id]))
        self.assertEqual(response.status_code, 302)  # redirect after delete
        self.assertEqual(Review.objects.count(), 0)

    def test_user_cannot_edit_someone_elses_review(self):
        """A logged-in user cannot edit another user's review"""
        other_user = User.objects.create_user(username="otheruser", password="password123")
        review = Review.objects.create(user=other_user, rating=4, comment="Nice place")
        
        self.client.login(username="tester", password="password123")
        response = self.client.post(reverse("edit_review", args=[review.id]), {
            "rating": 1,
            "comment": "I hacked this review"
        })
        # Should return 404 since get_object_or_404 checks ownership
        self.assertEqual(response.status_code, 404)
        review.refresh_from_db()
        self.assertEqual(review.comment, "Nice place")  # unchanged

    def test_user_cannot_delete_someone_elses_review(self):
        """A logged-in user cannot delete another user's review"""
        other_user = User.objects.create_user(username="otheruser", password="password123")
        review = Review.objects.create(user=other_user, rating=3, comment="Average experience")
        
        self.client.login(username="tester", password="password123")
        response = self.client.post(reverse("delete_review", args=[review.id]))
        # Should return 404 since get_object_or_404 checks ownership
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Review.objects.count(), 1)  # still exists