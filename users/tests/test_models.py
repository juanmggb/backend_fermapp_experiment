"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_email_successfull(self):
        email = "test@email.com"
        password = "test1234"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        sample_emails = [
            ("test1@EXAMPLE.COM", "test1@example.com"),
            ("Test2@Example.Com", "Test2@example.com"),
            ("TEST3@EXAMPLE.COM", "TEST3@example.com"),
            ("test4@example.COM", "test4@example.com"),
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password="test1234"
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test1234")

    def test_create_supuer_user(self):
        user = get_user_model().objects.create_superuser("test@email.com", "test1234")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
