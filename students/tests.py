
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from allocations.models import Allocation
from rooms.models import Hostel, Room
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
        self.assertTrue(StudentForm(data=self.valid_data()).is_valid())

    def test_invalid_phone(self):
        self.assertFalse(
            StudentForm(data=self.valid_data(phone="123")).is_valid()
        )

    def test_non_digit_phone(self):
        self.assertFalse(
            StudentForm(data=self.valid_data(phone="12345abcde")).is_valid()
        )

    def test_invalid_academic_year(self):
        self.assertFalse(
            StudentForm(data=self.valid_data(academic_year=5)).is_valid()
        )

    def test_missing_required_fields(self):
        self.assertFalse(StudentForm(data={}).is_valid())


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

    # --- add student ---

    def test_admin_can_open_add_student_form(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_anonymous_user_is_redirected_to_login(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_non_admin_is_forbidden(self):
        self.client.force_login(self.regular_user)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_valid_post_creates_student(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.url, self.valid_student_data())
        self.assertRedirects(response, self.list_url)
        self.assertTrue(
            Student.objects.filter(usn="1AB23CS006").exists()
        )

    def test_success_message_is_displayed(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.url, self.valid_student_data())
        self.assertRedirects(
            response, self.list_url, fetch_redirect_response=False
        )
        self.assertContains(
            self.client.get(self.list_url),
            "Student added successfully.",
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
                email="dup030@example.com",
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

    # --- student list ---

    def test_student_list_requires_login(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 302)

    def test_admin_can_view_student_list(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.list_url).status_code, 200)

    def test_non_admin_is_forbidden_from_student_list(self):
        self.client.force_login(self.regular_user)
        self.assertEqual(self.client.get(self.list_url).status_code, 403)

    # --- student detail ---

    def test_admin_can_view_student_detail(self):
        student = Student.objects.create(
            usn="1AB23CS050",
            name="Detail Student",
            email="detail@example.com",
            phone="9876543250",
            department="Computer Science",
            academic_year=1,
        )
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("student_detail", args=[student.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail Student")
        self.assertContains(response, "1AB23CS050")

    def test_non_admin_is_forbidden_from_student_detail(self):
        student = Student.objects.create(
            usn="1AB23CS050",
            name="Detail Student",
            email="detail@example.com",
            phone="9876543250",
            department="Computer Science",
            academic_year=1,
        )
        self.client.force_login(self.regular_user)
        response = self.client.get(
            reverse("student_detail", args=[student.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_nonexistent_student_returns_404(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("student_detail", args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    # --- update student ---

    def test_update_success_message_is_displayed(self):
        student = Student.objects.create(
            usn="1AB23CS020",
            name="Msg Student",
            email="msg.student@example.com",
            phone="9876543220",
            department="Computer Science",
            academic_year=2,
        )
        self.client.force_login(self.admin)
        detail_url = reverse("student_detail", args=[student.pk])
        response = self.client.post(
            reverse("student_update", args=[student.pk]),
            {
                "usn": "1AB23CS020",
                "name": "Msg Student",
                "email": "msg.student@example.com",
                "phone": "9876543220",
                "department": "Computer Science",
                "academic_year": 2,
            },
        )
        self.assertRedirects(
            response, detail_url, fetch_redirect_response=False
        )
        self.assertContains(
            self.client.get(detail_url),
            "Student updated successfully.",
        )

    def test_admin_can_update_student(self):
        student = Student.objects.create(
            usn="1AB23CS010",
            name="Old Name",
            email="old.name@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=2,
        )
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("student_update", args=[student.pk]),
            {
                "usn": "1AB23CS010",
                "name": "Updated Name",
                "email": "updated.name@example.com",
                "phone": "9876543211",
                "department": "Information Science",
                "academic_year": 3,
            },
        )
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.name, "Updated Name")
        self.assertEqual(student.department, "Information Science")

    def test_invalid_update_does_not_save(self):
        student = Student.objects.create(
            usn="1AB23CS011",
            name="Original Name",
            email="original.name@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=2,
        )
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("student_update", args=[student.pk]),
            {
                "usn": "1AB23CS011",
                "name": "Changed Name",
                "email": "original.name@example.com",
                "phone": "123",
                "department": "Computer Science",
                "academic_year": 5,
            },
        )
        self.assertEqual(response.status_code, 200)
        student.refresh_from_db()
        self.assertEqual(student.name, "Original Name")

    def test_non_admin_cannot_update_student(self):
        student = Student.objects.create(
            usn="1AB23CS012",
            name="Protected Student",
            email="protected.student@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=2,
        )
        self.client.force_login(self.regular_user)
        response = self.client.get(
            reverse("student_update", args=[student.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_update_student(self):
        student = Student.objects.create(
            usn="1AB23CS013",
            name="Private Student",
            email="private.student@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=2,
        )
        response = self.client.get(
            reverse("student_update", args=[student.pk])
        )
        self.assertEqual(response.status_code, 302)

    # --- delete student ---

    def test_admin_can_delete_student(self):
        student = Student.objects.create(
            usn="1AB23CS060",
            name="Delete Me",
            email="delete.me@example.com",
            phone="9876543260",
            department="Computer Science",
            academic_year=1,
        )
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("student_delete", args=[student.pk])
        )
        self.assertRedirects(
            response, self.list_url, fetch_redirect_response=False
        )
        self.assertFalse(
            Student.objects.filter(pk=student.pk).exists()
        )

    def test_get_request_does_not_delete_student(self):
        student = Student.objects.create(
            usn="1AB23CS061",
            name="No Delete Get",
            email="nodelete.get@example.com",
            phone="9876543261",
            department="Computer Science",
            academic_year=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("student_delete", args=[student.pk])
        )
        self.assertEqual(response.status_code, 405)
        self.assertTrue(
            Student.objects.filter(pk=student.pk).exists()
        )

    def test_non_admin_cannot_delete_student(self):
        student = Student.objects.create(
            usn="1AB23CS062",
            name="Protected Delete",
            email="protected.delete@example.com",
            phone="9876543262",
            department="Computer Science",
            academic_year=1,
        )
        self.client.force_login(self.regular_user)
        response = self.client.post(
            reverse("student_delete", args=[student.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Student.objects.filter(pk=student.pk).exists()
        )

    def test_anonymous_user_cannot_delete_student(self):
        student = Student.objects.create(
            usn="1AB23CS063",
            name="Anon Delete",
            email="anon.delete@example.com",
            phone="9876543263",
            department="Computer Science",
            academic_year=1,
        )
        response = self.client.post(
            reverse("student_delete", args=[student.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Student.objects.filter(pk=student.pk).exists()
        )

    # --- search ---

    def test_search_returns_matching_students(self):
        Student.objects.create(
            usn="1AB23CS070",
            name="Alice Smith",
            email="alice@example.com",
            phone="9876543270",
            department="Computer Science",
            academic_year=1,
        )
        Student.objects.create(
            usn="1AB23CS071",
            name="Bob Jones",
            email="bob@example.com",
            phone="9876543271",
            department="Information Science",
            academic_year=2,
        )
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url, {"q": "Alice"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertNotContains(response, "Bob Jones")

    def test_search_by_department(self):
        Student.objects.create(
            usn="1AB23CS072",
            name="Carol White",
            email="carol@example.com",
            phone="9876543272",
            department="Mechanical Engineering",
            academic_year=3,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            self.list_url, {"q": "Mechanical"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carol White")

    def test_empty_search_returns_all_students(self):
        Student.objects.create(
            usn="1AB23CS073",
            name="Dave Brown",
            email="dave@example.com",
            phone="9876543273",
            department="Computer Science",
            academic_year=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url, {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dave Brown")

    def test_search_no_results(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            self.list_url, {"q": "zzznomatch"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No matching students found")

    def test_search_by_usn_partial(self):
        Student.objects.create(
            usn="1AB23CS074",
            name="Eve Taylor",
            email="eve@example.com",
            phone="9876543274",
            department="Computer Science",
            academic_year=2,
        )
        Student.objects.create(
            usn="1AB23EC099",
            name="Unrelated USN",
            email="unrelated.usn@example.com",
            phone="9876543299",
            department="Civil Engineering",
            academic_year=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            self.list_url, {"q": "cs074"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eve Taylor")
        self.assertNotContains(response, "Unrelated USN")

    def test_search_by_email_partial(self):
        Student.objects.create(
            usn="1AB23CS075",
            name="Frank Green",
            email="frank.green@example.com",
            phone="9876543275",
            department="Computer Science",
            academic_year=1,
        )
        Student.objects.create(
            usn="1AB23EC098",
            name="Unrelated Email",
            email="other@example.com",
            phone="9876543298",
            department="Civil Engineering",
            academic_year=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            self.list_url, {"q": "FRANK.GREEN"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frank Green")
        self.assertNotContains(response, "Unrelated Email")

    def test_search_by_phone_partial(self):
        Student.objects.create(
            usn="1AB23CS076",
            name="Grace Hall",
            email="grace@example.com",
            phone="9876543276",
            department="Computer Science",
            academic_year=3,
        )
        Student.objects.create(
            usn="1AB23EC097",
            name="Unrelated Phone",
            email="other.phone@example.com",
            phone="1234567890",
            department="Civil Engineering",
            academic_year=1,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            self.list_url, {"q": "543276"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grace Hall")
        self.assertNotContains(response, "Unrelated Phone")

    def test_search_is_case_insensitive(self):
        Student.objects.create(
            usn="1AB23CS077",
            name="Henry King",
            email="henry@example.com",
            phone="9876543277",
            department="Computer Science",
            academic_year=2,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            self.list_url, {"q": "henry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Henry King")


class StudentRoomViewTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="room_admin",
            password="TestPassword!234",
            is_staff=True,
        )

        self.regular_user = User.objects.create_user(
            username="room_student",
            password="TestPassword!234",
            is_staff=False,
        )

        self.student = Student.objects.create(
            usn="1AB23CS100",
            name="Room Test Student",
            email="roomtest@example.com",
            phone="9876543210",
            department="Computer Science",
            academic_year=2,
        )

        self.hostel = Hostel.objects.create(
            name="HOSTEL-29 Test Hostel",
            block="A",
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="301",
            capacity=2,
            occupied_count=1,
        )

        self.url = reverse(
            "student_room",
            args=[self.student.pk],
        )

    def test_admin_can_view_active_room_details(self):
        self.client.force_login(self.admin)

        allocation = Allocation.objects.create(
            student=self.student,
            room=self.room,
            status=Allocation.Status.ACTIVE,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HOSTEL-29 Test Hostel")
        self.assertContains(response, "301")
        self.assertContains(response, "Allocation Date:")
        self.assertContains(
            response,
            str(allocation.allocated_at.year),
        )

    def test_vacate_room_button_appears_for_active_allocation(self):
        self.client.force_login(self.admin)

        Allocation.objects.create(
            student=self.student,
            room=self.room,
            status=Allocation.Status.ACTIVE,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        vacate_url = reverse(
            "allocations:vacate_room",
            args=[self.student.pk],
        )

        self.assertContains(response, f'href="{vacate_url}"')
        self.assertContains(response, "Vacate Room")

    def test_student_without_active_allocation_sees_empty_message(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Active Allocation")
        self.assertIsNone(response.context["allocation"])

    def test_inactive_allocation_is_not_displayed_as_current(self):
        self.client.force_login(self.admin)

        Allocation.objects.create(
            student=self.student,
            room=self.room,
            status=Allocation.Status.VACATED,
            vacated_at=timezone.now(),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["allocation"])
        self.assertContains(response, "No Active Allocation")

    def test_invalid_student_id_returns_404(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("student_room", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    def test_non_admin_cannot_view_room_details(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


# HOSTEL-33: Student Account Association and Portal Tests

class StudentPortalTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.student_user = User.objects.create_user(
            username="portal_student",
            password="PortalPass!234",
            is_staff=False,
        )

        self.unlinked_user = User.objects.create_user(
            username="unlinked_student",
            password="PortalPass!234",
            is_staff=False,
        )

        self.admin = User.objects.create_user(
            username="portal_admin",
            password="PortalPass!234",
            is_staff=True,
        )

        self.student = Student.objects.create(
            usn="1AB23CS201",
            name="Portal Test Student",
            email="portal.student@example.com",
            phone="9876543201",
            department="Computer Science",
            academic_year=2,
            user=self.student_user,
        )

        self.other_student = Student.objects.create(
            usn="1AB23CS202",
            name="Other Student",
            email="other.portal@example.com",
            phone="9876543202",
            department="Computer Science",
            academic_year=2,
        )

    def test_linked_student_can_access_own_portal(self):
        self.client.force_login(self.student_user)

        response = self.client.get(reverse("student_portal"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["student"], self.student)
        self.assertContains(response, "Portal Test Student")
        self.assertNotContains(response, "Other Student")

    def test_unlinked_account_receives_forbidden_response(self):
        self.client.force_login(self.unlinked_user)

        response = self.client.get(reverse("student_portal"))

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("student_portal"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_linked_student_can_access_own_room_page(self):
        self.client.force_login(self.student_user)

        response = self.client.get(reverse("student_portal_room"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["student"], self.student)
        self.assertIsNone(response.context["allocation"])
        self.assertContains(response, "No room allocated yet.")

    def test_unlinked_account_cannot_access_room_page(self):
        self.client.force_login(self.unlinked_user)

        response = self.client.get(reverse("student_portal_room"))

        self.assertEqual(response.status_code, 403)

    def test_student_account_cannot_access_admin_dashboard(self):
        self.client.force_login(self.student_user)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 403)

    def test_admin_dashboard_access_remains_unchanged(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_linked_student_can_see_own_active_allocation(self):
        hostel = Hostel.objects.create(
            name="Test Hostel",
            block="A",
        )

        room = Room.objects.create(
            hostel=hostel,
            room_number="101",
            capacity=3,
            occupied_count=1,
        )

        allocation = Allocation.objects.create(
            student=self.student,
            room=room,
            status=Allocation.Status.ACTIVE,
        )

        self.client.force_login(self.student_user)

        response = self.client.get(reverse("student_portal"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["allocation"], allocation)
        self.assertContains(response, "Test Hostel")
        self.assertContains(response, "101")
        self.assertContains(response, "ACTIVE")

    def test_student_cannot_access_another_students_record_using_query_parameter(self):
        self.client.force_login(self.student_user)

        response = self.client.get(
            reverse("student_portal"),
            {"student_id": self.other_student.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["student"], self.student)
        self.assertContains(response, "Portal Test Student")
        self.assertNotContains(response, "Other Student")
