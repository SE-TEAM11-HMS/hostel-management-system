
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Student


class StudentManagementIntegrationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="integrationadmin",
            password="TestPassword!234",
            is_staff=True,
        )

        self.login_url = reverse("accounts:login")
        self.add_url = reverse("student_add")
        self.list_url = reverse("student_list")

        self.student_data = {
            "usn": "1AB23CS090",
            "name": "Integration Student",
            "email": "integration.student@example.com",
            "phone": "9876543290",
            "department": "Computer Science",
            "academic_year": 2,
        }

    def test_login_add_and_retrieve_student(self):
        login_response = self.client.post(
            self.login_url,
            {
                "username": "integrationadmin",
                "password": "TestPassword!234",
            },
        )
        self.assertEqual(login_response.status_code, 302)

        add_response = self.client.post(
            self.add_url, self.student_data
        )
        self.assertEqual(add_response.status_code, 302)

        student = Student.objects.get(usn="1AB23CS090")
        detail_url = reverse("student_detail", args=[student.pk])
        detail_response = self.client.get(detail_url)

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Integration Student")
        self.assertEqual(
            Student.objects.get(pk=student.pk).email,
            "integration.student@example.com",
        )

    def test_update_student_and_verify_database(self):
        self.client.force_login(self.admin)
        student = Student.objects.create(**self.student_data)

        update_url = reverse("student_update", args=[student.pk])
        updated_data = {
            **self.student_data,
            "name": "Updated Integration Student",
            "email": "updated.integration@example.com",
        }

        response = self.client.post(update_url, updated_data)
        self.assertEqual(response.status_code, 302)

        student.refresh_from_db()
        self.assertEqual(student.name, "Updated Integration Student")
        self.assertEqual(
            student.email, "updated.integration@example.com"
        )

    def test_delete_student_and_verify_database(self):
        self.client.force_login(self.admin)
        student = Student.objects.create(**self.student_data)

        delete_url = reverse("student_delete", args=[student.pk])
        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())

    def test_unauthenticated_user_cannot_add_student(self):
        response = self.client.post(
            self.add_url, self.student_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Student.objects.filter(usn="1AB23CS090").exists()
        )

    def test_invalid_student_is_not_saved(self):
        self.client.force_login(self.admin)
        invalid_data = {
            **self.student_data,
            "phone": "invalid-phone",
            "academic_year": 5,
        }

        response = self.client.post(self.add_url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Student.objects.filter(usn="1AB23CS090").exists()
        )
