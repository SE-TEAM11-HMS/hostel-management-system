
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Student


User = get_user_model()


class StudentDataProtectionTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="security_admin",
            password="AdminPass123!",
            is_staff=True,
            is_superuser=True,
        )

        self.regular_user = User.objects.create_user(
            username="security_student",
            password="StudentPass123!",
            is_staff=False,
        )

        self.admin_client = Client()
        self.admin_client.force_login(self.admin)

        self.user_client = Client()
        self.user_client.force_login(self.regular_user)

        self.student = Student.objects.create(
            name="Test Student",
            usn="SEC001",
            email="security@example.com",
            phone="9876543210",
            department="CSE",
            academic_year=2,
        )

    def test_non_admin_cannot_add_student(self):
        self.user_client.post(
            reverse("student_add"),
            {
                "name": "Unauthorized Student",
                "usn": "SEC002",
                "email": "unauthorized@example.com",
                "phone": "9876543211",
                "department": "CSE",
                "academic_year": "2",
            },
        )

        self.assertFalse(
            Student.objects.filter(usn="SEC002").exists()
        )

    def test_non_admin_cannot_update_student(self):
        original_name = self.student.name

        self.user_client.post(
            reverse("student_update", args=[self.student.pk]),
            {
                "name": "Unauthorized Change",
                "usn": self.student.usn,
                "email": self.student.email,
                "phone": self.student.phone,
                "department": self.student.department,
                "academic_year": str(self.student.academic_year),
            },
        )

        self.student.refresh_from_db()
        self.assertEqual(self.student.name, original_name)

    def test_student_name_is_escaped_on_detail_page(self):
        self.student.name = "<script>alert('xss')</script>"
        self.student.save()

        response = self.admin_client.get(
            reverse("student_detail", args=[self.student.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            "<script>alert('xss')</script>",
            html=False,
        )

    def test_csrf_token_is_required_for_deletion(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.admin)

        response = csrf_client.post(
            reverse("student_delete", args=[self.student.pk])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Student.objects.filter(pk=self.student.pk).exists()
        )

    def test_invalid_email_is_not_saved_on_add(self):
        initial_count = Student.objects.count()

        self.admin_client.post(
            reverse("student_add"),
            {
                "name": "Invalid Email Student",
                "usn": "SEC003",
                "email": "not-an-email",
                "phone": "9876543212",
                "department": "CSE",
                "academic_year": "2",
            },
        )

        self.assertEqual(Student.objects.count(), initial_count)

    def test_injection_like_search_does_not_return_all_students(self):
        Student.objects.create(
            name="Another Student",
            usn="SEC004",
            email="another@example.com",
            phone="9876543213",
            department="ECE",
            academic_year=2,
        )

        response = self.admin_client.get(
            reverse("student_list"),
            {"q": "' OR '1'='1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Another Student")

    def test_invalid_email_does_not_update_existing_student(self):
        original_email = self.student.email

        self.admin_client.post(
            reverse("student_update", args=[self.student.pk]),
            {
                "name": self.student.name,
                "usn": self.student.usn,
                "email": "invalid-email",
                "phone": self.student.phone,
                "department": self.student.department,
                "academic_year": str(self.student.academic_year),
            },
        )

        self.student.refresh_from_db()
        self.assertEqual(self.student.email, original_email)

    def test_non_staff_cannot_delete_student(self):
        response = self.user_client.post(
            reverse("student_delete", args=[self.student.pk])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Student.objects.filter(pk=self.student.pk).exists()
        )

    def test_staff_non_superuser_can_view_student_list(self):
        staff_user = User.objects.create_user(
            username="security_staff",
            password="StaffPass123!",
            is_staff=True,
            is_superuser=False,
        )

        staff_client = Client()
        staff_client.force_login(staff_user)

        response = staff_client.get(reverse("student_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Student")
