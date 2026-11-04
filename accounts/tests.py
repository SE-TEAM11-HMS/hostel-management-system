
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from students.models import Student


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

    def test_admin_login_redirects_to_safe_next_url(self):
        next_url = reverse("accounts:dashboard")

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "hmsadmin",
                "password": "TestPassword!234",
                "next": next_url,
            },
        )

        self.assertRedirects(response, next_url)

    def test_admin_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "hmsadmin",
                "password": "TestPassword!234",
                "next": "https://evil.example.com/",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:dashboard"),
        )

    def test_invalid_password_is_rejected(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "hmsadmin",
                "password": "WrongPassword",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")
        self.assertNotIn("_auth_user_id", self.client.session)

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

        self.assertContains(response, "Invalid username or password.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/?next="))

    def test_non_admin_cannot_access_dashboard(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 403)

    def test_logout_terminates_session(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_does_not_accept_get_requests(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 405)


class StudentAuthenticationTests(TestCase):

    def setUp(self):
        self.password = "StudentPassword!234"

        self.student_user = User.objects.create_user(
            username="student01",
            password=self.password,
            is_staff=False,
        )

        self.student = Student.objects.create(
            usn="TEST001",
            name="Test Student",
            email="student01@example.com",
            phone="9876543210",
            department="CSE",
            academic_year=3,
            user=self.student_user,
        )

        self.unlinked_user = User.objects.create_user(
            username="unlinked",
            password=self.password,
            is_staff=False,
        )

        self.staff_user = User.objects.create_user(
            username="staffuser",
            password=self.password,
            is_staff=True,
        )

    def test_linked_student_can_login(self):
        response = self.client.post(
            reverse("accounts:student_login"),
            {
                "username": "student01",
                "password": self.password,
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:student_portal"),
        )
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.student_user.pk),
        )

    def test_unlinked_user_cannot_login_as_student(self):
        response = self.client.post(
            reverse("accounts:student_login"),
            {
                "username": "unlinked",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Invalid student username or password.",
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_staff_user_cannot_login_as_student(self):
        response = self.client.post(
            reverse("accounts:student_login"),
            {
                "username": "staffuser",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Invalid student username or password.",
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_student_can_access_own_portal(self):
        self.client.force_login(self.student_user)

        response = self.client.get(
            reverse("accounts:student_portal")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["student"], self.student)

    def test_unlinked_user_cannot_access_student_portal(self):
        self.client.force_login(self.unlinked_user)

        response = self.client.get(
            reverse("accounts:student_portal")
        )

        self.assertEqual(response.status_code, 403)

    def test_staff_user_cannot_access_student_portal(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("accounts:student_portal")
        )

        self.assertEqual(response.status_code, 403)

    def test_student_logout_terminates_session(self):
        self.client.force_login(self.student_user)

        response = self.client.post(
            reverse("accounts:student_logout")
        )

        self.assertRedirects(
            response,
            reverse("accounts:student_login"),
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_student_logout_does_not_accept_get_requests(self):
        self.client.force_login(self.student_user)

        response = self.client.get(
            reverse("accounts:student_logout")
        )

        self.assertEqual(response.status_code, 405)

    def test_student_user_relationship_persists(self):
        self.student.refresh_from_db()

        self.assertEqual(self.student.user, self.student_user)
        self.assertEqual(self.student_user.student, self.student)

    def test_student_cannot_access_another_students_record(self):
        another_user = User.objects.create_user(
            username="student02",
            password=self.password,
        )

        another_student = Student.objects.create(
            usn="TEST002",
            name="Another Student",
            email="student02@example.com",
            phone="9876543211",
            department="ECE",
            academic_year=2,
            user=another_user,
        )

        self.client.force_login(self.student_user)

        response = self.client.get(
            reverse("accounts:student_portal")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["student"], self.student)
        self.assertNotEqual(response.context["student"], another_student)
