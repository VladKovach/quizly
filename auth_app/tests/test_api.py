from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTestsHappy(APITestCase):
    def setUp(self):
        registration_url = reverse("register")
        registration_data = {
            "username": "username",
            "email": "your_email@example.com",
            "password": "examplePassword",
            "confirmed_password": "examplePassword",
        }
        self.registration_response = self.client.post(
            registration_url, registration_data
        )

    def test_registration_and_login_ok(self):
        """
        Ensure we can registrate and login.
        """

        registration_response = self.registration_response
        self.assertEqual(
            registration_response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            registration_response.data["detail"], "User created successfully!"
        )
        self.assertIn(
            "access_token",
            registration_response.cookies,
        )
        self.assertIn(
            "refresh_token",
            registration_response.cookies,
        )

        # login
        login_url = reverse("login")
        login_data = {"username": "username", "password": "examplePassword"}
        login_response = self.client.post(login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            login_response.data,
            {
                "detail": "Login successfully!",
                "user": {
                    "id": 1,
                    "username": "username",
                    "email": "your_email@example.com",
                },
            },
        )
        self.assertIn("access_token", login_response.cookies)
        self.assertIn("refresh_token", login_response.cookies)

    def test_refresh_token_ok(self):

        url = reverse("refresh")
        response = self.client.post(url)
        self.assertIn("access_token", response.cookies)

    def test_logout_ok(self):

        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.cookies["access_token"].value, "")
        self.assertEqual(response.cookies["refresh_token"].value, "")
        self.assertEqual(
            response.data["detail"],
            "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.",
        )


class AuthTestsUnHappy(APITestCase):

    def test_registration_with_invalid_fields_not_ok(self):
        """
        Ensure we can not registrate.
        """
        url = reverse("register")
        registration_data = {
            "username": "",
            "email": "@example.com",
            "password": "examplePassword",
            "confirmed_password": "examplePassword123",
        }
        registration_response = self.client.post(url, registration_data)
        self.assertEqual(
            registration_response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_duplicate_registration_not_ok(self):
        """
        Ensure we can not registrate existed user.
        """
        url = reverse("register")
        registration_data = {
            "username": "username",
            "email": "your_email@example.com",
            "password": "examplePassword",
            "confirmed_password": "examplePassword",
        }
        self.client.post(url, registration_data)
        registration_response = self.client.post(url, registration_data)
        self.assertEqual(
            registration_response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_login_not_ok(self):
        """
        Ensure we can not login.
        """
        url = reverse("register")
        registration_data = {
            "username": "username",
            "email": "your_email@example.com",
            "password": "examplePassword",
            "confirmed_password": "examplePassword",
        }
        self.client.post(url, registration_data)
        url = reverse("login")
        login_data = {
            "username": "username",
            "password": "examplePassword1123",
        }
        login_response = self.client.post(url, login_data)
        self.assertEqual(
            login_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_refresh_token_not_ok(self):

        url = reverse("refresh")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
