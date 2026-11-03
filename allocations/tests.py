
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.urls import reverse

from students.models import Student
from rooms.models import Hostel, Room
from rooms.services import RoomFullError, RoomNotFoundError

from .models import Allocation
from .admin import AllocationAdmin
from .services import (
    AllocationService,
    StudentNotFoundError,
    StudentAlreadyAllocatedError,
)


User = get_user_model()


class AllocationServiceTests(TestCase):

    def setUp(self):
        self.hostel = Hostel.objects.create(
            name="Allocation Test Hostel",
            block="A",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            capacity=2,
            occupied_count=0,
        )

        self.student = Student.objects.create(
            usn="TEST001",
            name="Test Student",
            email="test001@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=3,
        )

    def test_successful_room_allocation(self):
        allocation = AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.assertEqual(allocation.student, self.student)
        self.assertEqual(allocation.room, self.room)
        self.assertEqual(
            allocation.status,
            Allocation.Status.ACTIVE,
        )
        self.assertIsNone(allocation.vacated_at)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)

    def test_student_cannot_have_two_active_allocations(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        with self.assertRaises(StudentAlreadyAllocatedError):
            AllocationService.allocate_room(
                self.student.id,
                self.room.id,
            )

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)

        self.assertEqual(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).count(),
            1,
        )

    def test_full_room_rejects_allocation(self):
        self.room.occupied_count = self.room.capacity
        self.room.save()

        with self.assertRaises(RoomFullError):
            AllocationService.allocate_room(
                self.student.id,
                self.room.id,
            )

        self.room.refresh_from_db()
        self.assertEqual(
            self.room.occupied_count,
            self.room.capacity,
        )

        self.assertFalse(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).exists()
        )

    def test_nonexistent_student_is_rejected(self):
        with self.assertRaises(StudentNotFoundError):
            AllocationService.allocate_room(
                999999,
                self.room.id,
            )

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)

    def test_nonexistent_room_is_rejected(self):
        with self.assertRaises(RoomNotFoundError):
            AllocationService.allocate_room(
                self.student.id,
                999999,
            )

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)

        self.assertFalse(
            Allocation.objects.filter(
                student=self.student
            ).exists()
        )

    def test_allocation_creates_only_one_record(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.assertEqual(
            Allocation.objects.filter(
                student=self.student
            ).count(),
            1,
        )

    def test_failed_allocation_does_not_create_record(self):
        self.room.occupied_count = self.room.capacity
        self.room.save()

        with self.assertRaises(RoomFullError):
            AllocationService.allocate_room(
                self.student.id,
                self.room.id,
            )

        self.assertEqual(
            Allocation.objects.filter(
                student=self.student
            ).count(),
            0,
        )


class AllocationPermissionTests(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="allocation_admin",
            password="TestPassword!234",
            is_staff=True,
        )

        self.student_user = User.objects.create_user(
            username="allocation_student",
            password="TestPassword!234",
            is_staff=False,
        )

        self.hostel = Hostel.objects.create(
            name="Permission Test Hostel",
            block="B",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="201",
            capacity=2,
            occupied_count=0,
        )

        self.student = Student.objects.create(
            usn="TEST002",
            name="Permission Test Student",
            email="test002@example.com",
            phone="9876543211",
            department="Computer Science",
            academic_year=2,
        )

        self.url = reverse("allocations:allocate_room")

    def test_anonymous_user_cannot_allocate_room(self):
        response = self.client.post(
            self.url,
            {
                "student_id": self.student.id,
                "room_id": self.room.id,
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Allocation.objects.filter(
                student=self.student
            ).exists()
        )

    def test_normal_student_cannot_allocate_room(self):
        self.client.force_login(self.student_user)

        response = self.client.post(
            self.url,
            {
                "student_id": self.student.id,
                "room_id": self.room.id,
            },
        )

        self.assertEqual(response.status_code, 403)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)

        self.assertFalse(
            Allocation.objects.filter(
                student=self.student
            ).exists()
        )

    def test_admin_can_allocate_room(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            self.url,
            {
                "student_id": self.student.id,
                "room_id": self.room.id,
            },
        )

        self.assertRedirects(
            response,
            self.url,
        )

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)

        self.assertTrue(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).exists()
        )

    def test_admin_can_view_allocation_form(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Allocate Room to Student",
        )

    def test_malformed_student_id_is_handled(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            self.url,
            {
                "student_id": "abc",
                "room_id": self.room.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "does not exist")

    def test_malformed_room_id_is_handled(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            self.url,
            {
                "student_id": self.student.id,
                "room_id": "abc",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "does not exist")

    def test_allocation_endpoint_rejects_other_methods(self):
        self.client.force_login(self.admin_user)

        response = self.client.put(self.url)

        self.assertEqual(response.status_code, 405)


class AllocationAdminPermissionTests(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="allocation_admin_permissions",
            password="TestPassword!234",
            is_staff=True,
        )

        self.allocation_admin = AllocationAdmin(
            Allocation,
            admin.site,
        )

        self.request = RequestFactory().get(
            "/admin/allocations/allocation/"
        )
        self.request.user = self.admin_user

    def test_admin_cannot_add_allocation_directly(self):
        self.assertFalse(
            self.allocation_admin.has_add_permission(
                self.request
            )
        )

    def test_admin_cannot_change_allocation_directly(self):
        self.assertFalse(
            self.allocation_admin.has_change_permission(
                self.request
            )
        )

    def test_admin_cannot_delete_allocation_directly(self):
        self.assertFalse(
            self.allocation_admin.has_delete_permission(
                self.request
            )
        )
