"""
Tests for the yser API
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient


CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")
ME_URL = reverse("users:me")


def create_user(**kwargs):
    """Create adn return a new user"""

    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "test@email.com",
            "password": "test1234",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, 201)

        user = get_user_model().objects.get(email=payload["email"])

        self.assertTrue(user.check_password(payload["password"]))

        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        user_details = {
            "email": "test@email.com",
            "password": "test1234",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {
            "email": "test@email.com",
            "password": "test1234",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, 400)

    def test_create_token_for_user(self):
        user_details = {
            "email": "test@email.com",
            "password": "test1234",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {"email": "test@email.com", "password": "test1234"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("access", res.data)

        self.assertEqual(res.status_code, 200)

    def test_create_token_bad_credentials(self):
        user_details = {
            "email": "test@email.com",
            "password": "test1234",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {"email": "wrongemail@email.com", "password": "test1234"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, 401)

    def test_create_token_blank_password(self):
        payload = {"email": "test@email.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, 400)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, 401)


class PrivateUserApiTest(TestCase):
    def setUp(self):
        self.user = create_user(email="email@email.com", password="test1234", name="1")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["email"], self.user.email)

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, 405)

    def test_update_user_profile(self):
        payload = {"name": "Updated name", "password": "newpassword"}

        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
