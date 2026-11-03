
import threading
from queue import Queue
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib import admin
from django.db import close_old_connections, connection
from django.test import TestCase, TransactionTestCase, RequestFactory
from django.urls import reverse

from students.models import Student
from rooms.models import Hostel, Room
from rooms.services import (
    RoomFullError,
    RoomNotFoundError,
    RoomNotOccupiedError,
)

from .models import Allocation
from .admin import AllocationAdmin
from .services import (
    AllocationService,
    StudentNotFoundError,
    StudentAlreadyAllocatedError,
    ActiveAllocationNotFoundError,
    SameRoomError,
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

        self.new_room = Room.objects.create(
            hostel=self.hostel,
            room_number="102",
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

    # ALLOCATION TESTS

    def test_successful_room_allocation(self):
        allocation = AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.assertEqual(allocation.student, self.student)
        self.assertEqual(allocation.room, self.room)
        self.assertEqual(allocation.status, Allocation.Status.ACTIVE)
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

    # HOSTEL-30 ROOM CHANGE TESTS

    def test_successful_room_change(self):
        old_allocation = AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        new_allocation = AllocationService.change_room(
            self.student.id,
            self.new_room.id,
        )

        old_allocation.refresh_from_db()
        self.room.refresh_from_db()
        self.new_room.refresh_from_db()

        self.assertEqual(
            old_allocation.status,
            Allocation.Status.VACATED,
        )
        self.assertIsNotNone(old_allocation.vacated_at)

        self.assertEqual(
            new_allocation.status,
            Allocation.Status.ACTIVE,
        )
        self.assertEqual(new_allocation.room, self.new_room)

        self.assertEqual(self.room.occupied_count, 0)
        self.assertEqual(self.new_room.occupied_count, 1)

        self.assertEqual(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).count(),
            1,
        )

    def test_change_to_full_room_is_rejected(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.new_room.occupied_count = self.new_room.capacity
        self.new_room.save()

        with self.assertRaises(RoomFullError):
            AllocationService.change_room(
                self.student.id,
                self.new_room.id,
            )

        old_allocation = Allocation.objects.get(
            student=self.student,
            status=Allocation.Status.ACTIVE,
        )

        self.room.refresh_from_db()
        self.new_room.refresh_from_db()

        self.assertEqual(old_allocation.room, self.room)
        self.assertIsNone(old_allocation.vacated_at)
        self.assertEqual(self.room.occupied_count, 1)
        self.assertEqual(
            self.new_room.occupied_count,
            self.new_room.capacity,
        )

    def test_change_to_same_room_is_rejected(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        with self.assertRaises(SameRoomError):
            AllocationService.change_room(
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

    def test_change_room_without_active_allocation_is_rejected(self):
        with self.assertRaises(ActiveAllocationNotFoundError):
            AllocationService.change_room(
                self.student.id,
                self.new_room.id,
            )

        self.new_room.refresh_from_db()
        self.assertEqual(self.new_room.occupied_count, 0)

    def test_change_room_with_invalid_student_is_rejected(self):
        with self.assertRaises(StudentNotFoundError):
            AllocationService.change_room(
                999999,
                self.new_room.id,
            )

    def test_change_room_with_invalid_room_is_rejected(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        with self.assertRaises(RoomNotFoundError):
            AllocationService.change_room(
                self.student.id,
                999999,
            )

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)

    def test_room_change_rolls_back_if_old_room_release_fails(self):
        old_allocation = AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        with patch(
            "allocations.services.RoomService.release_bed",
            side_effect=RoomNotOccupiedError(
                "Simulated room release failure."
            ),
        ):
            with self.assertRaises(RoomNotOccupiedError):
                AllocationService.change_room(
                    self.student.id,
                    self.new_room.id,
                )

        old_allocation.refresh_from_db()
        self.room.refresh_from_db()
        self.new_room.refresh_from_db()

        self.assertEqual(
            old_allocation.status,
            Allocation.Status.ACTIVE,
        )
        self.assertIsNone(old_allocation.vacated_at)

        self.assertEqual(self.room.occupied_count, 1)
        self.assertEqual(self.new_room.occupied_count, 0)

        self.assertEqual(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).count(),
            1,
        )

    # HOSTEL-32 VACATION TESTS

    def test_successful_room_vacation(self):
        allocation = AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        vacated = AllocationService.vacate_room(
            self.student.id
        )

        allocation.refresh_from_db()
        self.room.refresh_from_db()

        self.assertEqual(vacated.id, allocation.id)
        self.assertEqual(
            allocation.status,
            Allocation.Status.VACATED,
        )
        self.assertIsNotNone(allocation.vacated_at)
        self.assertEqual(self.room.occupied_count, 0)

        self.assertFalse(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).exists()
        )

        # Previous allocation must remain as history.
        self.assertTrue(
            Allocation.objects.filter(
                pk=allocation.pk
            ).exists()
        )

    def test_repeated_vacation_is_rejected(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        AllocationService.vacate_room(self.student.id)

        with self.assertRaises(ActiveAllocationNotFoundError):
            AllocationService.vacate_room(self.student.id)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)

        self.assertEqual(
            Allocation.objects.filter(
                student=self.student,
            ).count(),
            1,
        )

    def test_vacation_without_active_allocation_is_rejected(self):
        with self.assertRaises(ActiveAllocationNotFoundError):
            AllocationService.vacate_room(self.student.id)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)

    def test_vacation_rolls_back_if_room_release_fails(self):
        allocation = AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        with patch(
            "allocations.services.RoomService.release_bed",
            side_effect=RoomNotOccupiedError(
                "Simulated room release failure."
            ),
        ):
            with self.assertRaises(RoomNotOccupiedError):
                AllocationService.vacate_room(self.student.id)

        allocation.refresh_from_db()
        self.room.refresh_from_db()

        self.assertEqual(
            allocation.status,
            Allocation.Status.ACTIVE,
        )
        self.assertIsNone(allocation.vacated_at)
        self.assertEqual(self.room.occupied_count, 1)


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

        self.new_room = Room.objects.create(
            hostel=self.hostel,
            room_number="202",
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
        self.change_url = reverse(
            "allocations:change_room",
            args=[self.student.id],
        )

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

        self.assertRedirects(response, self.url)

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

    # HOSTEL-30 VIEW PERMISSION TESTS

    def test_anonymous_user_cannot_change_room(self):
        response = self.client.post(
            self.change_url,
            {"room_id": self.new_room.id},
        )

        self.assertEqual(response.status_code, 302)

    def test_normal_student_cannot_change_room(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.client.force_login(self.student_user)

        response = self.client.post(
            self.change_url,
            {"room_id": self.new_room.id},
        )

        self.assertEqual(response.status_code, 403)

        self.room.refresh_from_db()
        self.new_room.refresh_from_db()

        self.assertEqual(self.room.occupied_count, 1)
        self.assertEqual(self.new_room.occupied_count, 0)

    def test_admin_can_view_change_room_page(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.client.force_login(self.admin_user)

        response = self.client.get(self.change_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student.name)

    def test_admin_can_change_student_room(self):
        AllocationService.allocate_room(
            self.student.id,
            self.room.id,
        )

        self.client.force_login(self.admin_user)

        response = self.client.post(
            self.change_url,
            {"room_id": self.new_room.id},
        )

        self.assertRedirects(response, self.change_url)

        self.room.refresh_from_db()
        self.new_room.refresh_from_db()

        self.assertEqual(self.room.occupied_count, 0)
        self.assertEqual(self.new_room.occupied_count, 1)

        self.assertTrue(
            Allocation.objects.filter(
                student=self.student,
                room=self.new_room,
                status=Allocation.Status.ACTIVE,
            ).exists()
        )


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


# HOSTEL-32 MYSQL CONCURRENCY TEST

class AllocationConcurrencyTests(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        if connection.vendor != "mysql":
            self.skipTest("This concurrency test requires MySQL.")

        self.hostel = Hostel.objects.create(
            name="Concurrency Test Hostel",
            block="C",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="301",
            capacity=1,
            occupied_count=0,
        )

        self.student1 = Student.objects.create(
            usn="CONC001",
            name="Concurrency Student One",
            email="conc001@example.com",
            phone="9876543212",
            department="Computer Science",
            academic_year=3,
        )

        self.student2 = Student.objects.create(
            usn="CONC002",
            name="Concurrency Student Two",
            email="conc002@example.com",
            phone="9876543213",
            department="Computer Science",
            academic_year=3,
        )

    def test_only_one_student_gets_last_available_bed(self):
        results = Queue()
        start_barrier = threading.Barrier(2)

        def allocate(student_id):
            close_old_connections()

            try:
                start_barrier.wait(timeout=15)

                AllocationService.allocate_room(
                    student_id,
                    self.room.id,
                )

                results.put("SUCCESS")

            except RoomFullError:
                results.put("FULL")

            except Exception as error:
                results.put(
                    f"ERROR: {type(error).__name__}: {error}"
                )

            finally:
                close_old_connections()

        threads = [
            threading.Thread(
                target=allocate,
                args=(self.student1.id,),
            ),
            threading.Thread(
                target=allocate,
                args=(self.student2.id,),
            ),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=30)

        self.assertTrue(
            all(not thread.is_alive() for thread in threads),
            "A concurrency test thread did not finish.",
        )

        outcomes = [
            results.get_nowait()
            for _ in threads
        ]

        self.assertCountEqual(
            outcomes,
            ["SUCCESS", "FULL"],
        )

        self.room.refresh_from_db()

        self.assertEqual(self.room.occupied_count, 1)

        self.assertEqual(
            Allocation.objects.filter(
                room=self.room,
                status=Allocation.Status.ACTIVE,
            ).count(),
            1,
        )
