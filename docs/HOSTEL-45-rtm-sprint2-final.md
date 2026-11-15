# Hostel Management System — Final Requirements Traceability Matrix (Sprint 2)

**Jira story:** HOSTEL-45  
**Sprint:** Sprint 2  
**Epic:** Documentation & Final Release  
**Prepared by:** Pradeep  
**GitHub issue:** #57

Status legend:
- **P** = Passed — requirement implemented and verified by automated test evidence
- **NT** = Not Tested — no automated or manual test evidence recorded
- **F** = Failed / Action Required — test executed but failed or defect open
- **B** = Blocked — cannot be tested due to a dependency or environment constraint

---

## 1. Functional Requirements

| Req ID | Requirement | Module / Implementation | Test Evidence | Sprint | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-F-001 | Administrator login with valid credentials | `accounts/views.py` — `LoginView` | `accounts/tests.py::LoginViewTest::test_valid_login_redirects_to_dashboard`; `students/test_regression.py::AuthenticationRegressionTests::test_admin_can_authenticate_and_open_dashboard` | 1 & 2 | P | Verified in CI runs #245, #280 |
| HMS-F-002 | Reject invalid login credentials | `accounts/views.py` — `LoginView` | `accounts/tests.py::LoginViewTest::test_invalid_password_shows_error`; `students/test_regression.py::AuthenticationRegressionTests::test_invalid_credentials_do_not_create_an_authenticated_session` | 1 & 2 | P | Generic error message; no session created |
| HMS-F-003 | Add student record | `students/views.py` — `StudentCreateView` | `students/tests.py::StudentViewTest::test_valid_post_creates_student`; `students/test_regression.py::StudentLifecycleRegressionTests::test_student_create_view_update_and_delete_lifecycle` | 1 & 2 | P | Duplicate USN/email rejected |
| HMS-F-004 | View student details | `students/views.py` — `StudentDetailView` | `students/tests.py::StudentViewTest::test_admin_can_view_student_detail` | 1 | P | 404 for non-existent student |
| HMS-F-005 | Update student record | `students/views.py` — `StudentUpdateView` | `students/tests.py::StudentViewTest::test_admin_can_update_student`; `students/test_regression.py::StudentLifecycleRegressionTests::test_student_create_view_update_and_delete_lifecycle` | 1 & 2 | P | Invalid data rejected without saving |
| HMS-F-006 | Remove student record | `students/views.py` — `StudentDeleteView` | `students/tests.py::StudentViewTest::test_admin_can_delete_student`; `students/test_regression.py::StudentLifecycleRegressionTests::test_student_create_view_update_and_delete_lifecycle` | 1 & 2 | P | GET returns 405; POST-only delete |
| HMS-F-007 | Add hostel and room details | `rooms/views.py` — `AddHostelView`, `AddRoomView` | `rooms/tests.py::RoomCreationTest`; `docs/HOSTEL-40-functional-test-report.md` | 2 | P | CI run #254 |
| HMS-F-008 | View available rooms | `rooms/views.py` — `AvailableRoomsView` | `rooms/tests.py::AvailableRoomsTest`; `students/test_regression.py::IntegratedRoomAndPortalRegressionTests` | 2 | P | CI run #254 |
| HMS-F-009 | View occupied rooms | `rooms/views.py` — `OccupiedRoomsView` | `rooms/tests.py::OccupiedRoomsTest`; `docs/HOSTEL-40-functional-test-report.md` | 2 | P | CI run #254 |
| HMS-F-010 | Allocate room to student | `allocations/views.py` — `AllocateRoomView`; `allocations/services.py` — `AllocationService.allocate_room` | `allocations/tests.py::AllocationTest::test_successful_allocation`; `students/test_regression.py::IntegratedRoomAndPortalRegressionTests::test_room_management_allocation_student_portal_and_vacation_work_together` | 2 | P | CI run #261, #280 |
| HMS-F-011 | Prevent allocation of a full room | `allocations/services.py` — capacity check | `allocations/tests.py::AllocationTest::test_full_room_rejected` | 2 | P | CI run #254 |
| HMS-F-012 | View allocated room details (admin) | `students/views.py` — `StudentRoomView` | `students/tests.py::StudentRoomViewTest::test_admin_can_view_active_room_details` | 2 | P | CI run #254 |
| HMS-F-013 | Change room allocation | `allocations/views.py` — `ChangeRoomView`; `allocations/services.py` — `AllocationService.change_room` | `allocations/tests.py::ChangeRoomTest`; `students/tests.py::StudentPortalTests::test_student_sees_new_room_after_room_change` | 2 | P | CI run #254 |
| HMS-F-014 | Vacate room | `allocations/views.py` — `VacateRoomView`; `allocations/services.py` — `AllocationService.vacate_room` | `allocations/tests.py::VacateRoomTest`; `students/test_regression.py::IntegratedRoomAndPortalRegressionTests` | 2 | P | History retained; CI run #280 |
| HMS-F-015 | Search student records | `students/views.py` — `StudentListView` (query param `q`) | `students/tests.py::StudentViewTest::test_search_returns_matching_students`; `students/test_regression.py::StudentLifecycleRegressionTests::test_student_search_returns_matching_record_without_unrelated_records` | 1 & 2 | P | Case-insensitive; USN, name, email, phone, department |
| HMS-F-016 | Update room availability (occupied_count) | `allocations/services.py` — increments/decrements `occupied_count` | `allocations/tests.py`; `docs/HOSTEL-41-mysql-integration-report.md` | 2 | P | Verified via MySQL integration CI run #261 |
| HMS-F-017 | View room details | `rooms/views.py` — `RoomDetailView` | `rooms/tests.py::RoomDetailTest`; `students/test_regression.py::IntegratedRoomAndPortalRegressionTests` | 2 | P | CI run #280 |

---

## 2. Security Requirements

| Req ID | Requirement | Module / Implementation | Test Evidence | Sprint | Status | Notes |
|---|---|---|---|---|---|---|
| HMS-SEC-001 | Authenticate users before granting access | `accounts/views.py`; `@login_required` decorators | `accounts/tests.py`; `students/test_regression.py::AuthenticationRegressionTests::test_admin_can_authenticate_and_open_dashboard` | 1 & 2 | P | CI run #245, #280 |
| HMS-SEC-002 | Reject invalid credentials with a generic message | `accounts/views.py` — `LoginView` | `students/test_regression.py::AuthenticationRegressionTests::test_invalid_credentials_do_not_create_an_authenticated_session`; `docs/HOSTEL-39-security-test-report.md` | 1 & 2 | P | No session created on failure |
| HMS-SEC-003 | Restrict administrative pages to staff users | `accounts/views.py`; `students/views.py`; `rooms/views.py`; `allocations/views.py` — `is_staff` checks | `students/test_regression.py::AuthenticationRegressionTests::test_student_account_remains_blocked_from_admin_dashboard`; `students/test_regression.py::AuthorizationRegressionTests::test_student_cannot_access_or_mutate_admin_student_and_room_records` | 1 & 2 | P | HTTP 403 for non-staff; CI run #245, #280 |
| HMS-SEC-004 | Protect data from unauthorized modification or deletion | `students/views.py`; `allocations/views.py` — permission checks | `students/test_security.py`; `students/test_regression.py::AuthorizationRegressionTests` | 1 & 2 | P | Student deletion and room allocation blocked for non-staff |
| HMS-SEC-005 | Terminate session on logout | `accounts/views.py` — `LogoutView` | `students/tests.py::StudentPortalTests::test_student_post_logout_terminates_session`; `docs/HOSTEL-39-security-test-report.md` | 1 & 2 | P | Session cleared; redirect to login |
| HMS-SEC-006 | Validate and sanitize input before storage | `students/forms.py`; `rooms/forms.py`; model `clean()` and `CheckConstraint` | `students/tests.py::StudentFormTest`; `rooms/test_room_validation.py`; `docs/HOSTEL-39-security-test-report.md` | 1 & 2 | P | Phone regex, academic year range, capacity ≥ 1 |

---

## 3. Non-Functional Requirements

| Req ID | Requirement | Evidence | Sprint | Status | Notes |
|---|---|---|---|---|---|
| HMS-NFR-001 | User-friendly interface | Manual review of login, dashboard, student directory, room management and student portal templates | 1 & 2 | P (assessed) | Formal accessibility/usability study not conducted; interface reviewed manually |
| HMS-NFR-002 | Response time within 3 seconds | `students/test_nonfunctional.py` — test-client timing; `docs/HOSTEL-42-non-functional-test-report.md` | 2 | P (assessed) | Test-client timing only; excludes browser rendering and network latency |
| HMS-NFR-003 | Data accuracy and consistency | `allocations/test_mysql_integration.py`; `docs/HOSTEL-41-mysql-integration-report.md` — rollback and FK enforcement | 2 | P | MySQL FK constraints and transaction rollback verified; CI run #261 |
| HMS-NFR-004 | System availability | `docs/HOSTEL-42-non-functional-test-report.md` — short CI availability probe | 2 | P (assessed) | Short probe only; sustained production uptime not measured |
| HMS-NFR-005 | Maintainability | Modular Django apps (`accounts`, `students`, `rooms`, `allocations`); automated test suite; CI pipeline | 1 & 2 | P (assessed) | Formal maintainability metric not measured |
| HMS-NFR-006 | Scalability | No formal load or concurrent-user test conducted | 2 | NT | Out of scope for academic project; noted as future work |

---

## 4. Acceptance Test Mapping (AT-001 to AT-016)

| AT ID | Requirement | Test description | Evidence | Status |
|---|---|---|---|---|
| AT-001 | HMS-SEC-001 | Administrator login | `students/test_regression.py::AuthenticationRegressionTests::test_admin_can_authenticate_and_open_dashboard` | P |
| AT-002 | HMS-SEC-002 | Invalid-credential rejection | `students/test_regression.py::AuthenticationRegressionTests::test_invalid_credentials_do_not_create_an_authenticated_session` | P |
| AT-003 | HMS-F-001 | Student creation | `students/tests.py::StudentViewTest::test_valid_post_creates_student` | P |
| AT-004 | HMS-F-015 | Student search | `students/test_regression.py::StudentLifecycleRegressionTests::test_student_search_returns_matching_record_without_unrelated_records` | P |
| AT-005 | HMS-F-005 | Student update and invalid-update | `students/tests.py::StudentViewTest::test_admin_can_update_student` | P |
| AT-006 | HMS-F-007 | Hostel and room creation | `rooms/tests.py::RoomCreationTest` | P |
| AT-007 | HMS-F-008 | Available-room listing | `rooms/tests.py::AvailableRoomsTest` | P |
| AT-008 | HMS-F-010 | Successful allocation | `allocations/tests.py::AllocationTest::test_successful_allocation` | P |
| AT-009 | HMS-F-011 | Full-room rejection | `allocations/tests.py::AllocationTest::test_full_room_rejected` | P |
| AT-010 | HMS-F-012 | Student allocated-room view | `students/tests.py::StudentRoomViewTest::test_admin_can_view_active_room_details` | P |
| AT-011 | HMS-F-013 | Room-change | `allocations/tests.py::ChangeRoomTest` | P |
| AT-012 | HMS-F-014 | Room-vacation | `students/test_regression.py::IntegratedRoomAndPortalRegressionTests::test_room_management_allocation_student_portal_and_vacation_work_together` | P |
| AT-013 | HMS-SEC-003 | Non-administrator dashboard denial | `students/test_regression.py::AuthorizationRegressionTests::test_student_cannot_access_or_mutate_admin_student_and_room_records` | P |
| AT-014 | HMS-NFR-002 | Representative operation timing | `students/test_nonfunctional.py`; `docs/HOSTEL-42-non-functional-test-report.md` | P |
| AT-015 | HMS-NFR-003 | Student update consistency | `students/tests.py::StudentViewTest::test_admin_can_update_student` | P |
| AT-016 | HMS-SEC-005 | Logout and protected-dashboard | `students/tests.py::StudentPortalTests::test_student_post_logout_terminates_session` | P |

---

## 5. Unverified Requirements

| Req ID | Reason |
|---|---|
| HMS-NFR-006 | Formal load/scalability testing is out of scope for this academic project. Noted as future work. |
| HMS-NFR-001 | Formal accessibility/usability study not conducted; manual review only. |

---

## 6. CI Evidence Summary

| CI Run | Activity | Result |
|---|---|---|
| [#245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) | Security testing (HOSTEL-39) | Passed |
| [#254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) | Functional room/allocation testing (HOSTEL-40) | Passed |
| [#261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521) | MySQL integration (HOSTEL-41) | Passed |
| [#270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) | Non-functional testing (HOSTEL-42) | Passed (with stated limits) |
| [#280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) | Acceptance testing AT-001–AT-016 (HOSTEL-43) | Passed |
