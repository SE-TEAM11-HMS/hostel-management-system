"""Integrated regression tests for HOSTEL-44.

These tests deliberately exercise the application through its public URLs and
service layer so the regression run covers cross-app behaviour, not only
isolated model operations.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from allocations.models import Allocation
from rooms.models import Hostel, Room
from students.models import Student


User = get_user_model()


class AuthenticationRegressionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="qa_regression_admin",
            password="RegressionPass!234",
            is_staff=True,
        )
        self.student_user = User.objects.create_user(
            username="qa_regression_student",
            password="RegressionPass!234",
            is_staff=False,
        )

    def test_admin_can_authenticate_and_open_dashboard(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "qa_regression_admin",
                "password": "RegressionPass!234",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertIn("_auth_user_id", self.client.session)

        dashboard = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(dashboard.status_code, 200)

    def test_invalid_credentials_do_not_create_an_authenticated_session(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "qa_regression_admin",
                "password": "IncorrectPassword!234",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_student_account_remains_blocked_from_admin_dashboard(self):
        self.client.force_login(self.student_user)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 403)


class StudentLifecycleRegressionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="qa_student_admin",
            password="RegressionPass!234",
            is_staff=True,
        )
        self.client.force_login(self.admin)

    def student_payload(self, **overrides):
        payload = {
            "usn": "QA24CS001",
            "name": "Regression Student",
            "email": "qa.student@example.com",
            "phone": "9876543210",
            "department": "Computer Science",
            "academic_year": 2,
        }
        payload.update(overrides)
        return payload

    def test_student_create_view_update_and_delete_lifecycle(self):
        create_response = self.client.post(
            reverse("student_add"),
            self.student_payload(),
        )
        self.assertRedirects(create_response, reverse("student_list"))

        student = Student.objects.get(usn="QA24CS001")

        detail_response = self.client.get(
            reverse("student_detail", args=[student.pk])
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Regression Student")

        update_response = self.client.post(
            reverse("student_update", args=[student.pk]),
            self.student_payload(
                name="Updated Regression Student",
                email="updated.qa.student@example.com",
                academic_year=3,
            ),
        )
        self.assertRedirects(
            update_response,
            reverse("student_detail", args=[student.pk]),
        )

        student.refresh_from_db()
        self.assertEqual(student.name, "Updated Regression Student")
        self.assertEqual(student.email, "updated.qa.student@example.com")
        self.assertEqual(student.academic_year, 3)

        delete_response = self.client.post(
            reverse("student_delete", args=[student.pk])
        )
        self.assertRedirects(delete_response, reverse("student_list"))
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())

    def test_student_search_returns_matching_record_without_unrelated_records(self):
        matching = Student.objects.create(
            usn="QASEARCH01",
            name="Matching QA Student",
            email="matching.qa@example.com",
            phone="9876543211",
            department="Computer Science",
            academic_year=2,
        )
        Student.objects.create(
            usn="QASEARCH02",
            name="Unrelated QA Student",
            email="unrelated.qa@example.com",
            phone="9876543212",
            department="Electronics",
            academic_year=3,
        )

        response = self.client.get(
            reverse("student_list"),
            {"q": matching.usn},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matching QA Student")
        self.assertNotContains(response, "Unrelated QA Student")
        self.assertEqual(list(response.context["students"]), [matching])


class AuthorizationRegressionTests(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(
            username="qa_access_student",
            password="RegressionPass!234",
            is_staff=False,
        )
        self.student = Student.objects.create(
            usn="QAACCESS01",
            name="Access Control Student",
            email="access.control@example.com",
            phone="9876543213",
            department="Computer Science",
            academic_year=2,
            user=self.student_user,
        )
        self.hostel = Hostel.objects.create(
            name="QA Access Hostel",
            block="QA",
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="QA-01",
            capacity=2,
        )

    def test_student_cannot_access_or_mutate_admin_student_and_room_records(self):
        self.client.force_login(self.student_user)

        protected_gets = (
            reverse("accounts:dashboard"),
            reverse("student_list"),
            reverse("rooms:room_list"),
            reverse("rooms:room_edit", args=[self.room.pk]),
        )
        for url in protected_gets:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

        delete_response = self.client.post(
            reverse("student_delete", args=[self.student.pk])
        )
        self.assertEqual(delete_response.status_code, 403)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

        allocation_response = self.client.post(
            reverse("allocations:allocate_room"),
            {
                "student_id": self.student.pk,
                "room_id": self.room.pk,
            },
        )
        self.assertEqual(allocation_response.status_code, 403)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)
        self.assertFalse(
            Allocation.objects.filter(student=self.student).exists()
        )


class IntegratedRoomAndPortalRegressionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="qa_integrated_admin",
            password="RegressionPass!234",
            is_staff=True,
        )
        self.student_user = User.objects.create_user(
            username="qa_integrated_student",
            password="RegressionPass!234",
            is_staff=False,
        )
        self.student = Student.objects.create(
            usn="QAINTEGRATION01",
            name="Integrated QA Student",
            email="integrated.qa@example.com",
            phone="9876543214",
            department="Computer Science",
            academic_year=2,
            user=self.student_user,
        )
        self.hostel = Hostel.objects.create(
            name="QA Integrated Hostel",
            block="INT",
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="INT-101",
            capacity=2,
        )

    def test_room_management_allocation_student_portal_and_vacation_work_together(self):
        self.client.force_login(self.admin)

        for url in (
            reverse("rooms:room_list"),
            reverse("rooms:available_rooms"),
            reverse("rooms:room_detail", args=[self.room.pk]),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

        allocation_response = self.client.post(
            reverse("allocations:allocate_room"),
            {
                "student_id": self.student.pk,
                "room_id": self.room.pk,
            },
        )
        self.assertEqual(allocation_response.status_code, 302)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)
        allocation = Allocation.objects.get(
            student=self.student,
            status=Allocation.Status.ACTIVE,
        )

        self.client.force_login(self.student_user)
        portal_response = self.client.get(reverse("student_portal_room"))

        self.assertEqual(portal_response.status_code, 200)
        self.assertEqual(portal_response.context["student"], self.student)
        self.assertEqual(portal_response.context["allocation"], allocation)
        self.assertContains(portal_response, "QA Integrated Hostel")
        self.assertContains(portal_response, "INT-101")

        self.client.force_login(self.admin)
        vacation_response = self.client.post(
            reverse(
                "allocations:vacate_room",
                args=[self.student.pk],
            ),
            {"confirm": "yes"},
        )
        self.assertEqual(vacation_response.status_code, 302)

        allocation.refresh_from_db()
        self.room.refresh_from_db()
        self.assertEqual(allocation.status, Allocation.Status.VACATED)
        self.assertIsNotNone(allocation.vacated_at)
        self.assertEqual(self.room.occupied_count, 0)
        self.assertTrue(
            Allocation.objects.filter(pk=allocation.pk).exists(),
            "Vacated allocation history must be retained.",
        )
