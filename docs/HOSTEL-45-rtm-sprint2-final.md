# Hostel Management System — Updated Requirements Traceability Matrix

## Project Information

Project: Hostel Management System
Team: 11
Jira story: HOSTEL-45
Sprint: Sprint 2
Status legend:
- P = Passed — requirement implemented and verified by automated test evidence
- NT = Not Tested — no automated or manual test evidence recorded
- A = Action Required — partially verified; further verification or action needed

---

## 1. Functional Requirements (HMS-F-001 to HMS-F-017)

### 1.1 Authentication (Sprint 1)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-F-001 | Administrator login with valid credentials | `accounts/views.py` — `LoginView` | `accounts/tests.py::LoginViewTest::test_valid_login_redirects_to_dashboard` | Automated test passed; CI run #245, #280 | P | Verified in Sprint 1 and Sprint 2 regression |
| HMS-F-002 | Reject invalid login credentials | `accounts/views.py` — `LoginView` | `accounts/tests.py::LoginViewTest::test_invalid_password_shows_error` | Automated test passed; CI run #245 | P | Generic error message; no session created |

### 1.2 Student Management (Sprint 1)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-F-003 | Add student record | `students/views.py` — `StudentCreateView` | `students/tests.py::StudentViewTest::test_valid_post_creates_student` | Automated test passed; CI run #245 | P | Duplicate USN and email rejected |
| HMS-F-004 | View student details | `students/views.py` — `StudentDetailView` | `students/tests.py::StudentViewTest::test_admin_can_view_student_detail` | Automated test passed; CI run #245 | P | Returns 404 for non-existent student |
| HMS-F-005 | Update student record | `students/views.py` — `StudentUpdateView` | `students/tests.py::StudentViewTest::test_admin_can_update_student` | Automated test passed; CI run #245 | P | Invalid data rejected without saving |
| HMS-F-006 | Remove student record | `students/views.py` — `StudentDeleteView` | `students/tests.py::StudentViewTest::test_admin_can_delete_student` | Automated test passed; CI run #245 | P | POST-only; GET returns 405 |
| HMS-F-015 | Search student records | `students/views.py` — `StudentListView` (`?q=`) | `students/tests.py::StudentViewTest::test_search_returns_matching_students` | Automated test passed; CI run #245 | P | Case-insensitive; searches USN, name, email, phone, department |

### 1.3 Room Management (Sprint 2)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-F-007 | Add hostel and room details | `rooms/views.py` — `AddHostelView`, `AddRoomView` | `rooms/tests.py::RoomCreationTest` | Automated test passed; CI run #254 | P | Unique room number per hostel enforced |
| HMS-F-008 | View available rooms | `rooms/views.py` — `AvailableRoomsView` | `rooms/tests.py::AvailableRoomsTest` | Automated test passed; CI run #254 | P | Lists rooms with available_beds > 0 |
| HMS-F-009 | View occupied rooms | `rooms/views.py` — `OccupiedRoomsView` | `rooms/tests.py::OccupiedRoomsTest` | Automated test passed; CI run #254 | P | Lists rooms with occupied_count > 0 |
| HMS-F-017 | View room details | `rooms/views.py` — `RoomDetailView` | `rooms/tests.py::RoomDetailTest` | Automated test passed; CI run #254, #280 | P | Shows room info and current allocations |

### 1.4 Room Allocation (Sprint 2)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-F-010 | Allocate room to student | `allocations/views.py` — `AllocateRoomView`; `allocations/services.py` — `AllocationService.allocate_room` | `allocations/tests.py::AllocationTest::test_successful_allocation` | Automated test passed; CI run #261, #280 | P | Occupancy incremented atomically |
| HMS-F-011 | Prevent allocation of a full room | `allocations/services.py` — capacity check before allocation | `allocations/tests.py::AllocationTest::test_full_room_rejected` | Automated test passed; CI run #254 | P | Returns error when available_beds = 0 |
| HMS-F-012 | View allocated room details | `students/views.py` — `StudentRoomView` | `students/tests.py::StudentRoomViewTest::test_admin_can_view_active_room_details` | Automated test passed; CI run #254 | P | Shows active allocation; None if no active allocation |
| HMS-F-013 | Change room allocation | `allocations/views.py` — `ChangeRoomView`; `allocations/services.py` — `AllocationService.change_room` | `allocations/tests.py::ChangeRoomTest`; `students/tests.py::StudentPortalTests::test_student_sees_new_room_after_room_change` | Automated tests passed; CI run #254 | P | Old allocation vacated; new allocation created atomically |
| HMS-F-014 | Vacate room | `allocations/views.py` — `VacateRoomView`; `allocations/services.py` — `AllocationService.vacate_room` | `allocations/tests.py::VacateRoomTest`; `students/test_regression.py::IntegratedRoomAndPortalRegressionTests::test_room_management_allocation_student_portal_and_vacation_work_together` | Automated tests passed; CI run #280 | P | History retained; occupancy decremented |
| HMS-F-016 | Update room availability (occupied_count) | `allocations/services.py` — increments/decrements `Room.occupied_count` | `allocations/test_mysql_integration.py` | Automated test passed; CI run #261 | P | Verified via MySQL integration tests |

### 1.5 Student Portal (Sprint 2)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-F-012 (portal) | Student views own allocated room | `students/views.py` — `StudentPortalRoomView` | `students/tests.py::StudentPortalTests::test_linked_student_can_see_own_active_allocation` | Automated test passed; CI run #280 | P | Student sees only their own allocation |

---

## 2. Security Requirements (HMS-SEC-001 to HMS-SEC-006)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-SEC-001 | Authenticate users before granting access | `accounts/views.py`; `@login_required` on all protected views | `accounts/tests.py::LoginViewTest::test_valid_login_redirects_to_dashboard`; `students/test_regression.py::AuthenticationRegressionTests::test_admin_can_authenticate_and_open_dashboard` | Automated tests passed; CI run #245, #280 | P | Unauthenticated requests redirected to login |
| HMS-SEC-002 | Reject invalid credentials with a generic message | `accounts/views.py` — `LoginView`; `django-axes` brute-force protection | `students/test_regression.py::AuthenticationRegressionTests::test_invalid_credentials_do_not_create_an_authenticated_session` | Automated test passed; CI run #245 | P | No session created; same message for wrong password and unknown user |
| HMS-SEC-003 | Restrict administrative pages to staff users only | `accounts/views.py`; `students/views.py`; `rooms/views.py`; `allocations/views.py` — `is_staff` checks | `students/test_regression.py::AuthenticationRegressionTests::test_student_account_remains_blocked_from_admin_dashboard`; `students/test_regression.py::AuthorizationRegressionTests::test_student_cannot_access_or_mutate_admin_student_and_room_records` | Automated tests passed; CI run #245, #280 | P | HTTP 403 returned for non-staff users |
| HMS-SEC-004 | Protect student and room data from unauthorized modification or deletion | `students/views.py`; `allocations/views.py` — permission checks on all mutation views | `students/test_security.py`; `students/test_regression.py::AuthorizationRegressionTests` | Automated tests passed; CI run #245, #280 | P | Student deletion and room allocation blocked for non-staff |
| HMS-SEC-005 | Terminate session on logout and restrict access to protected pages | `accounts/views.py` — `LogoutView` (POST-only); `AuthenticatedNoCacheMiddleware` | `students/tests.py::StudentPortalTests::test_student_post_logout_terminates_session` | Automated test passed; CI run #245 | P | Session cleared; back-button access prevented via no-cache headers |
| HMS-SEC-006 | Validate and sanitize all user input before storage | `students/forms.py`; `rooms/forms.py`; model `clean()` methods; `CheckConstraint` on models | `students/tests.py::StudentFormTest`; `rooms/test_room_validation.py` | Automated tests passed; CI run #245, #254 | P | Phone 10-digit regex, academic year 1–4, room capacity ≥ 1 |

---

## 3. Non-Functional Requirements (HMS-NFR-001 to HMS-NFR-006)

| Requirement ID | Requirement | System Module | Test Case | Test Evidence | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-NFR-001 | User-friendly interface | All templates — login, dashboard, student management, room management, student portal | `students/test_nonfunctional.py::TC-NFR-001` — interface rendering and heading checks | CI run #270 | A | Automated rendering checks passed. Formal usability or accessibility study not conducted; manual review only |
| HMS-NFR-002 | Response time within 3 seconds for normal operations | All views | `students/test_nonfunctional.py::TC-NFR-002` — timed dashboard, student list, available rooms and allocation form | CI run #270; all operations under 3-second threshold | P | Test-client timing only; excludes browser rendering and external network latency |
| HMS-NFR-003 | Data accuracy and consistency | `allocations/services.py`; MySQL FK constraints; transaction rollback | `allocations/test_mysql_integration.py::TC-NFR-003` — allocation and vacation consistency; rollback verification | CI run #261, #270 | P | MySQL FK enforcement and transaction rollback verified |
| HMS-NFR-004 | System availability during operational hours | Django application server; MySQL database | `students/test_nonfunctional.py::TC-NFR-004` — 20-request availability probe | CI run #270; all probe requests passed | A | Short CI probe only; sustained production uptime monitoring not conducted |
| HMS-NFR-005 | Maintainability — modular, testable codebase | Four Django apps (`accounts`, `students`, `rooms`, `allocations`); automated test suite; CI pipeline | `students/test_nonfunctional.py::TC-NFR-005` — full regression suite execution | CI run #270; complete automated suite passed | P | Formal maintainability metric not measured; modular structure and test coverage assessed |
| HMS-NFR-006 | Scalability — acceptable performance as data grows | `students/views.py` — `StudentListView` | `students/test_nonfunctional.py::TC-NFR-006` — student list at 25, 250 and 500 records | CI run #270; all dataset sizes returned under threshold | P | Concurrent-load testing not conducted; dataset-size scaling verified only |

---

## 4. Acceptance Test Mapping (AT-001 to AT-016)

| AT ID | Linked Requirement | Test Description | Test Case / Evidence | Status |
|---|---|---|---|---|
| AT-001 | HMS-SEC-001 | Administrator login with valid credentials | `students/test_regression.py::AuthenticationRegressionTests::test_admin_can_authenticate_and_open_dashboard` | P |
| AT-002 | HMS-SEC-002 | Invalid-credential rejection | `students/test_regression.py::AuthenticationRegressionTests::test_invalid_credentials_do_not_create_an_authenticated_session` | P |
| AT-003 | HMS-F-003 | Student record creation | `students/tests.py::StudentViewTest::test_valid_post_creates_student` | P |
| AT-004 | HMS-F-015 | Student search by USN | `students/test_regression.py::StudentLifecycleRegressionTests::test_student_search_returns_matching_record_without_unrelated_records` | P |
| AT-005 | HMS-F-005 | Student record update and invalid-update rejection | `students/tests.py::StudentViewTest::test_admin_can_update_student` | P |
| AT-006 | HMS-F-007 | Hostel and room creation | `rooms/tests.py::RoomCreationTest` | P |
| AT-007 | HMS-F-008 | Available-room listing | `rooms/tests.py::AvailableRoomsTest` | P |
| AT-008 | HMS-F-010 | Successful room allocation | `allocations/tests.py::AllocationTest::test_successful_allocation` | P |
| AT-009 | HMS-F-011 | Full-room allocation rejection | `allocations/tests.py::AllocationTest::test_full_room_rejected` | P |
| AT-010 | HMS-F-012 | Admin view of student allocated room | `students/tests.py::StudentRoomViewTest::test_admin_can_view_active_room_details` | P |
| AT-011 | HMS-F-013 | Room change | `allocations/tests.py::ChangeRoomTest` | P |
| AT-012 | HMS-F-014 | Room vacation and history retention | `students/test_regression.py::IntegratedRoomAndPortalRegressionTests::test_room_management_allocation_student_portal_and_vacation_work_together` | P |
| AT-013 | HMS-SEC-003 | Non-administrator denied access to admin dashboard | `students/test_regression.py::AuthorizationRegressionTests::test_student_cannot_access_or_mutate_admin_student_and_room_records` | P |
| AT-014 | HMS-NFR-002 | Representative operation response time | `students/test_nonfunctional.py::TC-NFR-002` | P |
| AT-015 | HMS-NFR-003 | Student update data consistency | `students/tests.py::StudentViewTest::test_admin_can_update_student` | P |
| AT-016 | HMS-SEC-005 | Logout terminates session; protected pages inaccessible | `students/tests.py::StudentPortalTests::test_student_post_logout_terminates_session` | P |

---

## 5. Requirements with Action Required or Not Tested

| Requirement ID | Status | Reason | Action |
|---|---|---|---|
| HMS-NFR-001 | A | Automated rendering checks passed; formal usability or accessibility study not conducted | Manual review completed; formal study deferred as future work |
| HMS-NFR-004 | A | Short CI availability probe passed; sustained production uptime monitoring not conducted | Deployment-level monitoring required for production release |

---

## 6. CI Evidence Summary

| CI Run | Activity | Result |
|---|---|---|
| [#39745586188](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/39745586188) | Sprint 1 — authentication and student management (62 tests) | Passed |
| [#245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) | Security testing — HOSTEL-39 | Passed |
| [#254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) | Functional room and allocation testing — HOSTEL-40 | Passed |
| [#261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521) | MySQL integration testing — HOSTEL-41 | Passed |
| [#270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) | Non-functional testing — HOSTEL-42 | Passed (with stated limits) |
| [#280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) | Acceptance testing AT-001 to AT-016 — HOSTEL-43 | Passed |

---

## 7. Notes

1. P indicates the listed test evidence passed in the referenced CI run.
2. NT indicates the requirement has not been tested; no evidence exists.
3. A indicates the requirement was partially verified; further verification or action is required.
4. All statuses reflect actual test results and CI evidence, not assumptions.
5. Sprint 1 RTM is retained in `docs/RTM_Sprint1.md` for reference.
6. This document supersedes the Sprint 1 RTM for Sprint 2 final traceability.
