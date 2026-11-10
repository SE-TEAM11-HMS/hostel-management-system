from datetime import timedelta
from unittest.mock import patch

from axes.models import AccessAttempt
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from hostel_project.settings import env_flag, env_positive_int


User = get_user_model()


class SecurityConfigurationTests(SimpleTestCase):

    def test_security_headers_are_present_on_login_page(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(
            response.headers["X-Content-Type-Options"],
            "nosniff",
        )
        self.assertEqual(
            response.headers["X-Frame-Options"],
            "DENY",
        )
        self.assertEqual(
            response.headers["Referrer-Policy"],
            "same-origin",
        )

    def test_environment_flag_accepts_explicit_boolean_values(self):
        for value, expected in (
            ("true", True),
            ("YES", True),
            ("1", True),
            ("false", False),
            ("OFF", False),
            ("0", False),
        ):
            with self.subTest(value=value), patch.dict(
                "os.environ",
                {"HOSTEL_TEST_FLAG": value},
            ):
                self.assertIs(
                    env_flag("HOSTEL_TEST_FLAG", default=True),
                    expected,
                )

    def test_environment_flag_rejects_ambiguous_values(self):
        with patch.dict("os.environ", {"HOSTEL_TEST_FLAG": "sometimes"}):
            with self.assertRaises(ImproperlyConfigured):
                env_flag("HOSTEL_TEST_FLAG")

    def test_positive_integer_environment_setting_rejects_invalid_values(self):
        for value in ("zero", "0", "-2"):
            with self.subTest(value=value), patch.dict(
                "os.environ",
                {"HOSTEL_TEST_LIMIT": value},
            ):
                with self.assertRaises(ImproperlyConfigured):
                    env_positive_int("HOSTEL_TEST_LIMIT", 5)


class AuthenticatedResponseCacheTests(TestCase):

    def test_authenticated_admin_response_is_not_cached(self):
        admin = User.objects.create_user(
            username="cache_admin",
            password="CachePass!234",
            is_staff=True,
        )
        self.client.force_login(admin)

        response = self.client.get(reverse("accounts:dashboard"))

        cache_control = response.headers["Cache-Control"].lower()
        self.assertIn("private", cache_control)
        self.assertIn("no-store", cache_control)
        self.assertIn("no-cache", cache_control)


class FailedLoginThrottleTests(TestCase):

    def setUp(self):
        AccessAttempt.objects.all().delete()
        self.admin = User.objects.create_user(
            username="throttle_admin",
            password="ThrottlePass!234",
            is_staff=True,
        )

    @override_settings(
        AXES_FAILURE_LIMIT=5,
        AXES_COOLOFF_TIME=timedelta(minutes=15),
        AXES_USE_ATTEMPT_EXPIRATION=True,
        AXES_LOCKOUT_PARAMETERS=[["username", "ip_address"]],
    )
    def test_repeated_failed_logins_are_temporarily_blocked(self):
        login_url = reverse("accounts:login")
        response = None

        for _ in range(5):
            response = self.client.post(
                login_url,
                {
                    "username": "throttle_admin",
                    "password": "WrongPassword!234",
                },
            )
            if response.status_code == 429:
                break
            self.assertEqual(response.status_code, 200)

        if response.status_code != 429:
            response = self.client.post(
                login_url,
                {
                    "username": "throttle_admin",
                    "password": "WrongPassword!234",
                },
            )

        self.assertEqual(response.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)


class CsrfProtectionTests(TestCase):

    def test_logout_post_without_csrf_token_is_rejected(self):
        admin = User.objects.create_user(
            username="csrf_admin",
            password="CsrfPass!234",
            is_staff=True,
        )
        client = Client(enforce_csrf_checks=True)
        client.force_login(admin)

        response = client.post(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 403)
        self.assertIn("_auth_user_id", client.session)


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

    def test_password_is_stored_using_django_hashing(self):
        self.assertNotEqual(self.admin.password, "TestPassword!234")
        self.assertTrue(self.admin.check_password("TestPassword!234"))

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
