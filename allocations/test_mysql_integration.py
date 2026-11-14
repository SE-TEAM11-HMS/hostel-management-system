from django.db import IntegrityError, connection, transaction
from django.test import TestCase

from allocations.models import Allocation
from allocations.services import AllocationService
from rooms.models import Hostel, Room
from rooms.services import RoomFullError
from students.models import Student


class MySQLIntegrationAndConsistencyTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            usn="MYSQL001",
            name="MySQL Integration Student",
            email="mysql001@example.com",
            phone="9876543210",
            department="CSE",
            academic_year=2,
        )
        self.hostel = Hostel.objects.create(
            name="MySQL Integration Hostel",
            block="A",
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            capacity=2,
        )
        self.full_room = Room.objects.create(
            hostel=self.hostel,
            room_number="102",
            capacity=1,
            occupied_count=1,
        )

    def test_uses_mysql_and_migrated_application_tables(self):
        self.assertEqual(connection.vendor, "mysql")

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            self.assertEqual(cursor.fetchone()[0], 1)

        table_names = set(connection.introspection.table_names())
        self.assertTrue(
            {
                "students_student",
                "rooms_hostel",
                "rooms_room",
                "allocations_allocation",
            }.issubset(table_names)
        )

    def test_student_hostel_room_and_allocation_persist_and_retrieve(self):
        allocation = AllocationService.allocate_room(
            self.student.pk,
            self.room.pk,
        )

        retrieved_student = Student.objects.get(pk=self.student.pk)
        retrieved_hostel = Hostel.objects.get(pk=self.hostel.pk)
        retrieved_room = Room.objects.get(pk=self.room.pk)
        retrieved_allocation = Allocation.objects.select_related(
            "student",
            "room",
            "room__hostel",
        ).get(pk=allocation.pk)

        self.assertEqual(retrieved_student.usn, "MYSQL001")
        self.assertEqual(retrieved_hostel.name, "MySQL Integration Hostel")
        self.assertEqual(retrieved_room.room_number, "101")
        self.assertEqual(retrieved_allocation.student, retrieved_student)
        self.assertEqual(retrieved_allocation.room, retrieved_room)
        self.assertEqual(
            retrieved_allocation.status,
            Allocation.Status.ACTIVE,
        )

    def test_active_allocations_match_room_occupancy_after_allocation(self):
        AllocationService.allocate_room(self.student.pk, self.room.pk)

        self.room.refresh_from_db()
        active_allocation_count = Allocation.objects.filter(
            room=self.room,
            status=Allocation.Status.ACTIVE,
        ).count()

        self.assertEqual(self.room.occupied_count, active_allocation_count)
        self.assertEqual(self.room.available_beds, 1)

    def test_vacation_releases_occupancy_and_preserves_history(self):
        allocation = AllocationService.allocate_room(
            self.student.pk,
            self.room.pk,
        )

        AllocationService.vacate_room(self.student.pk)

        allocation.refresh_from_db()
        self.room.refresh_from_db()

        self.assertEqual(allocation.status, Allocation.Status.VACATED)
        self.assertIsNotNone(allocation.vacated_at)
        self.assertEqual(self.room.occupied_count, 0)
        self.assertEqual(
            Allocation.objects.filter(
                room=self.room,
                status=Allocation.Status.ACTIVE,
            ).count(),
            0,
        )
        self.assertTrue(Allocation.objects.filter(pk=allocation.pk).exists())

    def test_failed_allocation_rolls_back_without_partial_records(self):
        with self.assertRaises(RoomFullError):
            AllocationService.allocate_room(
                self.student.pk,
                self.full_room.pk,
            )

        self.full_room.refresh_from_db()
        self.assertEqual(self.full_room.occupied_count, 1)
        self.assertFalse(
            Allocation.objects.filter(
                student=self.student,
                status=Allocation.Status.ACTIVE,
            ).exists()
        )

    def test_database_foreign_key_rejects_invalid_allocation_reference(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Allocation.objects.create(
                    student_id=999999,
                    room=self.room,
                    status=Allocation.Status.ACTIVE,
                )

        self.assertFalse(Allocation.objects.filter(room=self.room).exists())
