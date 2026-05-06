from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from urllib import response

class AuthAppPositiveTestCase(TestCase):
    def setUp(self):

        self.user_data = {
            "username": "test@example.com",
            "email": "test@example.com",
            "password": "testpassword123",
            "confirmed_password": "testpassword123",
        }

        self.registration_url = reverse("register")
        self.login_url = reverse("login")
        self.refresh_url = reverse("token_refresh")
        self.logout_url = reverse("logout")
        self.password_reset_url = reverse("password_reset")
        
    def test_user_registration(self):
        response = self.client.post(self.registration_url, self.user_data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("user", response.data)
        self.assertIn("token", response.data)

        self.assertEqual(response.data["user"]["email"], self.user_data["email"])
        self.assertTrue(len(response.data["token"]) > 0)
        self.assertIsInstance(response.data["token"], str)

        User = get_user_model()
        self.assertTrue(User.objects.filter(
            email=self.user_data["email"]).exists())

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

    def test_user_login(self):
        self.client.post(self.registration_url, self.user_data)

        User = get_user_model()
        user = User.objects.get(email=self.user_data["email"])
        user.is_active = True
        user.save()

        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

