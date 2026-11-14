from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Student


class StudentSearchFunctionalTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username="functional_search_admin",
            password="FunctionalPass!234",
            is_staff=True,
        )
        self.matching_student = Student.objects.create(
            usn="SEARCH001",
            name="Search Match",
            email="search.match@example.com",
            phone="9876543210",
            department="CSE",
            academic_year=2,
        )
        Student.objects.create(
            usn="SEARCH002",
            name="Unrelated Student",
            email="unrelated@example.com",
            phone="9876543211",
            department="ECE",
            academic_year=3,
        )

    def test_admin_search_returns_only_matching_student(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("student_list"),
            {"q": self.matching_student.usn},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search Match")
        self.assertNotContains(response, "Unrelated Student")
        self.assertEqual(
            list(response.context["students"]),
            [self.matching_student],
        )
