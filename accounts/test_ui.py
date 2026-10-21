from django.test import TestCase
from django.urls import reverse


class AuthenticationUITests(TestCase):
    def test_login_renders_shared_styles_and_field_errors(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "", "password": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "css/app.css")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, 'role="alert"')
