
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import HostelForm, RoomForm
from .models import Hostel, Room


class RoomValidationTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="validation_admin",
            password="Admin@123",
            is_staff=True,
        )

        self.student = User.objects.create_user(
            username="validation_student",
            password="Student@123",
            is_staff=False,
        )

        self.hostel = Hostel.objects.create(
            name="Validation Hostel",
            block="A Block",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            capacity=4,
            occupied_count=2,
        )

        self.client.force_login(self.admin)

    def test_hostel_required_fields_are_validated(self):
        form = HostelForm(data={
            "name": "",
            "block": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("block", form.errors)

    def test_room_required_fields_are_validated(self):
        form = RoomForm(data={
            "hostel": "",
            "room_number": "",
            "capacity": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("hostel", form.errors)
        self.assertIn("room_number", form.errors)
        self.assertIn("capacity", form.errors)

    def test_zero_capacity_is_rejected(self):
        form = RoomForm(data={
            "hostel": self.hostel.id,
            "room_number": "102",
            "capacity": "0",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_negative_capacity_is_rejected(self):
        form = RoomForm(data={
            "hostel": self.hostel.id,
            "room_number": "102",
            "capacity": "-1",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_fractional_capacity_is_rejected(self):
        form = RoomForm(data={
            "hostel": self.hostel.id,
            "room_number": "102",
            "capacity": "2.5",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_nonnumeric_capacity_is_rejected(self):
        form = RoomForm(data={
            "hostel": self.hostel.id,
            "room_number": "102",
            "capacity": "abc",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_duplicate_room_number_case_insensitive(self):
        form = RoomForm(data={
            "hostel": self.hostel.id,
            "room_number": "101",
            "capacity": "4",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("room_number", form.errors)

    def test_room_number_can_be_reused_in_another_hostel(self):
        another_hostel = Hostel.objects.create(
            name="Another Hostel",
            block="B Block",
        )

        form = RoomForm(data={
            "hostel": another_hostel.id,
            "room_number": "101",
            "capacity": "3",
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_editing_room_does_not_flag_itself_as_duplicate(self):
        form = RoomForm(
            data={
                "hostel": self.hostel.id,
                "room_number": "101",
                "capacity": "4",
            },
            instance=self.room,
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_capacity_cannot_be_reduced_below_occupancy(self):
        response = self.client.post(
            reverse("rooms:room_edit", args=[self.room.id]),
            {
                "hostel": self.hostel.id,
                "room_number": "101",
                "capacity": "1",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("capacity", response.context["form"].errors)

        self.room.refresh_from_db()
        self.assertEqual(self.room.capacity, 4)
        self.assertEqual(self.room.occupied_count, 2)
        self.assertEqual(self.room.room_number, "101")

    def test_invalid_edit_does_not_partially_update_room(self):
        response = self.client.post(
            reverse("rooms:room_edit", args=[self.room.id]),
            {
                "hostel": self.hostel.id,
                "room_number": "999",
                "capacity": "1",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.room.refresh_from_db()
        self.assertEqual(self.room.room_number, "101")
        self.assertEqual(self.room.capacity, 4)

    def test_capacity_can_be_reduced_to_current_occupancy(self):
        response = self.client.post(
            reverse("rooms:room_edit", args=[self.room.id]),
            {
                "hostel": self.hostel.id,
                "room_number": "101",
                "capacity": "2",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.room.refresh_from_db()
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.occupied_count, 2)

    def test_non_admin_cannot_edit_room(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("rooms:room_edit", args=[self.room.id]),
            {
                "hostel": self.hostel.id,
                "room_number": "101",
                "capacity": "4",
            },
        )

        self.assertEqual(response.status_code, 403)

        self.room.refresh_from_db()
        self.assertEqual(self.room.capacity, 4)
