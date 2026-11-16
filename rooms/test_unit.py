"""Unit tests for room and hostel model behavior that needs no database."""

from django.test import SimpleTestCase

from rooms.models import Hostel, Room


class HostelModelUnitTests(SimpleTestCase):
    def test_hostel_string_representation_includes_name_and_block(self):
        hostel = Hostel(name="North Hostel", block="A")

        self.assertEqual(str(hostel), "North Hostel - A")


class RoomModelUnitTests(SimpleTestCase):
    def test_available_beds_is_capacity_minus_occupancy(self):
        room = Room(capacity=4, occupied_count=1)

        self.assertEqual(room.available_beds, 3)

    def test_full_room_has_no_available_beds(self):
        room = Room(capacity=2, occupied_count=2)

        self.assertEqual(room.available_beds, 0)

    def test_room_string_representation_includes_hostel_and_room_number(self):
        hostel = Hostel(name="North Hostel", block="A")
        room = Room(
            hostel=hostel,
            room_number="A-101",
            capacity=2,
            occupied_count=0,
        )

        self.assertEqual(str(room), "North Hostel - Room A-101")
