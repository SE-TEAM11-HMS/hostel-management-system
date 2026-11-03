
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase

from .models import Hostel, Room
from .services import (
    RoomService,
    RoomFullError,
    RoomNotFoundError,
    RoomNotOccupiedError,
)


class RoomServiceTests(TestCase):

    def setUp(self):
        self.hostel = Hostel.objects.create(
            name="Test Hostel",
            block="A",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            capacity=2,
            occupied_count=0,
        )

    def test_reserve_bed_increases_occupancy_once(self):
        updated_room = RoomService.reserve_bed(self.room.id)

        self.assertEqual(updated_room.occupied_count, 1)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)

    def test_reserve_bed_rejects_full_room(self):
        self.room.occupied_count = 2
        self.room.save()

        with self.assertRaises(RoomFullError):
            RoomService.reserve_bed(self.room.id)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 2)

    def test_reserve_bed_rejects_last_bed_after_full(self):
        self.room.occupied_count = 1
        self.room.save()

        RoomService.reserve_bed(self.room.id)

        with self.assertRaises(RoomFullError):
            RoomService.reserve_bed(self.room.id)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 2)

    def test_release_bed_decreases_occupancy_once(self):
        self.room.occupied_count = 2
        self.room.save()

        updated_room = RoomService.release_bed(self.room.id)

        self.assertEqual(updated_room.occupied_count, 1)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)

    def test_release_bed_rejects_empty_room(self):
        with self.assertRaises(RoomNotOccupiedError):
            RoomService.release_bed(self.room.id)

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 0)

    def test_reserve_bed_rejects_nonexistent_room(self):
        with self.assertRaises(RoomNotFoundError):
            RoomService.reserve_bed(999999)

    def test_release_bed_rejects_nonexistent_room(self):
        with self.assertRaises(RoomNotFoundError):
            RoomService.release_bed(999999)

    def test_occupancy_never_exceeds_capacity(self):
        self.room.occupied_count = 1
        self.room.save()

        RoomService.reserve_bed(self.room.id)

        with self.assertRaises(RoomFullError):
            RoomService.reserve_bed(self.room.id)

        self.room.refresh_from_db()
        self.assertLessEqual(
            self.room.occupied_count,
            self.room.capacity,
        )

    def test_occupancy_never_becomes_negative(self):
        with self.assertRaises(RoomNotOccupiedError):
            RoomService.release_bed(self.room.id)

        self.room.refresh_from_db()
        self.assertGreaterEqual(self.room.occupied_count, 0)


class ConcurrentRoomReservationTests(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.hostel = Hostel.objects.create(
            name="Concurrent Test Hostel",
            block="B",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="201",
            capacity=1,
            occupied_count=0,
        )

    def test_two_users_cannot_reserve_the_last_bed(self):
        barrier = Barrier(2)
        room_id = self.room.id

        def reserve_concurrently():
            close_old_connections()

            try:
                barrier.wait(timeout=10)

                try:
                    RoomService.reserve_bed(room_id)
                    return "reserved"
                except RoomFullError:
                    return "full"

            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(reserve_concurrently)
                for _ in range(2)
            ]

            results = [
                future.result(timeout=30)
                for future in futures
            ]

        self.assertCountEqual(
            results,
            ["reserved", "full"],
        )

        self.room.refresh_from_db()

        self.assertEqual(self.room.occupied_count, 1)
        self.assertLessEqual(
            self.room.occupied_count,
            self.room.capacity,
        )
