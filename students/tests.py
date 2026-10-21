
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import StudentForm
from .models import Student


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

    def test_user_relationship_is_optional(self):
        student = Student.objects.create(
            usn="1AB23CS040",
            name="Unlinked Student",
            email="unlinked@example.com",
            phone="9876543240",
            department="Computer Science",
            academic_year=1,
        )

        self.assertIsNone(student.user)


class StudentFormTest(TestCase):
    def valid_data(self, **overrides):
        data = {
            "usn": "1AB23CS003",
            "name": "Another Student",
            "email": "another.student@example.com",
            "phone": "9876543211",
            "department": "Computer Science",
            "academic_year": 2,
        }
        data.update(overrides)
        return data

    def test_valid_student_form(self):
        form = StudentForm(data=self.valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_phone(self):
        form = StudentForm(data=self.valid_data(phone="123"))
        self.assertFalse(form.is_valid())

    def test_non_digit_phone(self):
        form = StudentForm(data=self.valid_data(phone="12345abcde"))
        self.assertFalse(form.is_valid())

    def test_invalid_academic_year(self):
        form = StudentForm(data=self.valid_data(academic_year=5))
        self.assertFalse(form.is_valid())

    def test_missing_required_fields(self):
        form = StudentForm(data={})
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
        self.list_url = reverse("student_list")

    def valid_student_data(self, **overrides):
        data = {
            "usn": "1AB23CS006",
            "name": "Created Student",
            "email": "created.student@example.com",
            "phone": "9876543212",
            "department": "Computer Science",
            "academic_year": 2,
        }
        data.update(overrides)
        return data

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
        response = self.client.post(
            self.url, self.valid_student_data()
        )

        self.assertRedirects(response, self.list_url)
        self.assertTrue(
            Student.objects.filter(usn="1AB23CS006").exists()
        )

    def test_success_message_is_displayed(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            self.url, self.valid_student_data()
        )

        self.assertRedirects(response, self.list_url, fetch_redirect_response=False)

        list_response = self.client.get(self.list_url)
        self.assertContains(
            list_response, "Student added successfully."
        )

    def test_duplicate_usn_does_not_create_student(self):
        Student.objects.create(
            usn="1AB23CS030",
            name="Existing Student",
            email="existing030@example.com",
            phone="9876543230",
            department="Computer Science",
            academic_year=2,
        )

        self.client.force_login(self.admin)
        response = self.client.post(
            self.url,
            self.valid_student_data(
                usn="1AB23CS030",
                email="duplicate030@example.com",
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)

    def test_duplicate_email_does_not_create_student(self):
        Student.objects.create(
            usn="1AB23CS031",
            name="Existing Student",
            email="existing031@example.com",
            phone="9876543232",
            department="Computer Science",
            academic_year=2,
        )

        self.client.force_login(self.admin)
        response = self.client.post(
            self.url,
            self.valid_student_data(
                usn="1AB23CS032",
                email="existing031@example.com",
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)

    def test_missing_required_fields_do_not_create_student(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            self.url,
            {
                "usn": "",
                "name": "",
                "email": "",
                "phone": "",
                "department": "",
                "academic_year": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)

    def test_invalid_post_does_not_create_student(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            self.url,
            self.valid_student_data(academic_year=5),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)

    def test_student_list_requires_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)

    def test_admin_can_view_student_list(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
