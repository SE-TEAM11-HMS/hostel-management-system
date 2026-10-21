from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Student


class StudentManagementUITests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username="ui-admin",
            is_staff=True,
        )
        self.client.force_login(self.admin)

    def test_student_list_uses_shared_navigation_and_stylesheet(self):
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "css/app.css")
        self.assertContains(response, 'aria-label="Main navigation"')
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Students")

    def test_invalid_student_form_shows_field_specific_errors(self):
        response = self.client.post(
            reverse("student_add"),
            {
                "usn": "1AB23CS990",
                "name": "UI Test Student",
                "email": "ui.test.student@example.com",
                "phone": "invalid-phone",
                "department": "Computer Science",
                "academic_year": 5,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Phone number must contain exactly 10 digits.",
        )
        self.assertContains(
            response,
            "Academic year must be between 1 and 4.",
        )
        self.assertFalse(
            Student.objects.filter(usn="1AB23CS990").exists()
        )
