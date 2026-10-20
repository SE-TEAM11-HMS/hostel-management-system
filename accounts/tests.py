from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AdminAuthenticationTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="hmsadmin",
            password="TestPassword!234",
            is_staff=True,
        )

        self.student = User.objects.create_user(
            username="regularuser",
            password="TestPassword!234",
            is_staff=False,
        )

    def test_valid_admin_credentials_allow_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "hmsadmin",
                "password": "TestPassword!234",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:dashboard"),
        )

        self.assertIn("_auth_user_id", self.client.session)

    def test_invalid_password_is_rejected(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "hmsadmin",
                "password": "WrongPassword",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Invalid username or password.",
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_blank_fields_are_rejected(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "",
                "password": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_non_admin_cannot_use_admin_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "regularuser",
                "password": "TestPassword!234",
            },
        )

        self.assertContains(
            response,
            "Invalid username or password.",
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(
            reverse("accounts:dashboard")
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/?next="))

    def test_non_admin_cannot_access_dashboard(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("accounts:dashboard")
        )

        self.assertEqual(response.status_code, 403)

    def test_logout_terminates_session(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_logout_does_not_accept_get_requests(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("accounts:logout")
        )

        self.assertEqual(response.status_code, 405)