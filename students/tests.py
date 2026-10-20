
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Student
from .forms import StudentForm


class StudentModelTest(TestCase):
    def test_create_student(self):
        student = Student.objects.create(
            usn="1AB23CS002",
            name="Test Student",
            email="test.student@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=2,
        )

        self.assertEqual(student.name, "Test Student")
        self.assertEqual(str(student), "1AB23CS002 - Test Student")


class StudentFormTest(TestCase):
    def test_valid_student_form(self):
        form = StudentForm(data={
            "usn": "1AB23CS003",
            "name": "Another Student",
            "email": "another.student@example.com",
            "phone": "9876543211",
            "department": "Computer Science",
            "academic_year": 2,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form = StudentForm(data={
            "usn": "1AB23CS004",
            "name": "Phone Test",
            "email": "phone.test@example.com",
            "phone": "123",
            "department": "Computer Science",
            "academic_year": 2,
        })
        self.assertFalse(form.is_valid())

    def test_invalid_academic_year(self):
        form = StudentForm(data={
            "usn": "1AB23CS005",
            "name": "Year Test",
            "email": "year.test@example.com",
            "phone": "9876543210",
            "department": "Computer Science",
            "academic_year": 5,
        })
        self.assertFalse(form.is_valid())


class StudentViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="testadmin",
            password="TestAdminPass!234",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="testuser",
            password="TestUserPass!234",
            is_staff=False,
        )
        self.url = reverse("student_add")

    def test_admin_can_open_add_student_form(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_non_admin_is_forbidden(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_valid_post_creates_student(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.url, {
            "usn": "1AB23CS006",
            "name": "Created Student",
            "email": "created.student@example.com",
            "phone": "9876543212",
            "department": "Computer Science",
            "academic_year": 2,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Student.objects.filter(usn="1AB23CS006").exists()
        )
