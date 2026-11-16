"""End-to-end system test for the administrator and student workflows."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from allocations.models import Allocation
from rooms.models import Hostel, Room
from students.models import Student


User = get_user_model()


class HostelManagementSystemWorkflowTests(TestCase):
    """Exercise a complete room lifecycle through the public web interface."""

    def setUp(self):
        self.admin_password = "SystemAdminPass!234"
        self.student_password = "SystemStudentPass!234"
        self.admin = User.objects.create_user(
            username="system_test_admin",
            password=self.admin_password,
            is_staff=True,
        )
        self.student_user = User.objects.create_user(
            username="system_test_student",
            password=self.student_password,
            is_staff=False,
        )
        self.student = Student.objects.create(
            usn="SYS24CS001",
            name="System Test Student",
            email="system.student@example.com",
            phone="9876501234",
            department="Computer Science",
            academic_year=2,
            user=self.student_user,
        )
        self.hostel = Hostel.objects.create(
            name="System Test Hostel",
            block="SYS",
        )
        self.original_room = Room.objects.create(
            hostel=self.hostel,
            room_number="SYS-101",
            capacity=1,
        )
        self.replacement_room = Room.objects.create(
            hostel=self.hostel,
            room_number="SYS-102",
            capacity=1,
        )

    def sign_in_as_admin(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": self.admin.username,
                "password": self.admin_password,
            },
        )
        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_admin_to_student_allocation_change_portal_and_vacation(self):
        # The administrator signs in and can access the main workflows.
        self.sign_in_as_admin()
        self.assertEqual(
            self.client.get(reverse("accounts:dashboard")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("rooms:room_list")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("rooms:available_rooms")).status_code,
            200,
        )

        # Allocate a room through the allocation page.
        allocation_response = self.client.post(
            reverse("allocations:allocate_room"),
            {
                "student_id": self.student.pk,
                "room_id": self.original_room.pk,
            },
        )
        self.assertRedirects(
            allocation_response,
            reverse("allocations:allocate_room"),
        )
        self.original_room.refresh_from_db()
        self.assertEqual(self.original_room.occupied_count, 1)
        allocation = Allocation.objects.get(
            student=self.student,
            status=Allocation.Status.ACTIVE,
        )

        # Log out the administrator and authenticate through the student login.
        self.client.post(reverse("accounts:logout"))
        student_login_response = self.client.post(
            reverse("accounts:student_login"),
            {
                "username": self.student_user.username,
                "password": self.student_password,
            },
        )
        self.assertRedirects(
            student_login_response,
            reverse("student_portal"),
        )
        portal_response = self.client.get(reverse("student_portal"))
        self.assertEqual(portal_response.status_code, 200)
        self.assertContains(portal_response, "System Test Student")
        room_response = self.client.get(reverse("student_portal_room"))
        self.assertEqual(room_response.status_code, 200)
        self.assertContains(room_response, "System Test Hostel")
        self.assertContains(room_response, "SYS-101")

        # Sign back in as administrator and change the assigned room.
        self.client.post(reverse("accounts:logout"))
        self.sign_in_as_admin()
        change_response = self.client.post(
            reverse(
                "allocations:change_room",
                args=[self.student.pk],
            ),
            {"room_id": self.replacement_room.pk},
        )
        self.assertRedirects(
            change_response,
            reverse(
                "allocations:change_room",
                args=[self.student.pk],
            ),
        )
        allocation.refresh_from_db()
        self.original_room.refresh_from_db()
        self.replacement_room.refresh_from_db()
        self.assertEqual(allocation.status, Allocation.Status.VACATED)
        self.assertEqual(self.original_room.occupied_count, 0)
        self.assertEqual(self.replacement_room.occupied_count, 1)

        # The changed room is visible in the student portal.
        self.client.post(reverse("accounts:logout"))
        student_login_response = self.client.post(
            reverse("accounts:student_login"),
            {
                "username": self.student_user.username,
                "password": self.student_password,
            },
        )
        self.assertRedirects(
            student_login_response,
            reverse("student_portal"),
        )
        changed_room_response = self.client.get(
            reverse("student_portal_room")
        )
        self.assertEqual(changed_room_response.status_code, 200)
        self.assertContains(changed_room_response, "SYS-102")

        # Finally, the administrator vacates the room and occupancy is released.
        self.client.post(reverse("accounts:logout"))
        self.sign_in_as_admin()
        vacation_response = self.client.post(
            reverse(
                "allocations:vacate_room",
                args=[self.student.pk],
            ),
            {"confirm": "yes"},
        )
        self.assertRedirects(
            vacation_response,
            reverse("allocations:allocate_room"),
        )
        active_allocations = Allocation.objects.filter(
            student=self.student,
            status=Allocation.Status.ACTIVE,
        )
        self.assertFalse(active_allocations.exists())
        self.replacement_room.refresh_from_db()
        self.assertEqual(self.replacement_room.occupied_count, 0)
        self.assertTrue(
            Allocation.objects.filter(
                pk=allocation.pk,
                status=Allocation.Status.VACATED,
            ).exists()
        )
