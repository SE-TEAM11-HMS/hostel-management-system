# Hostel Management System — Sprint 2 Final RTM (HOSTEL-45)

## Project information

- Project: Hostel Management System
- Team: 11
- Document: Requirements Traceability Matrix — Sprint 2 Final
- Supersedes: `docs/RTM_Sprint1.md` (Sprint 1 RTM)
- Status legend: **P** = Passed · **NT** = Not Tested · **A** = Action Required (automated evidence exists; a stated limitation prevents full verification)

---

## 1. Functional requirements — Sprint 1 scope (HMS-F-001 to HMS-F-006, HMS-F-015)

Sprint 1 CI evidence: GitHub Actions [run #40696524346](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346) — 61 tests passed.

| Req ID | Requirement | Implementation | STP test case | Actual test identifier | CI evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| HMS-F-001 | Administrator login | `accounts/views.py::admin_login`; `accounts/forms.py::AdminLoginForm` | TC-001 | `accounts/tests.py::AdminAuthenticationTests.test_valid_admin_credentials_allow_login` | Run #40696524346 | P |
| HMS-F-002 | Invalid login handling | `accounts/views.py::admin_login`; `accounts/forms.py::AdminLoginForm` | TC-002 | `accounts/tests.py::AdminAuthenticationTests.test_invalid_password_is_rejected`; `test_blank_fields_are_rejected`; `test_non_admin_cannot_use_admin_login` | Run #40696524346 | P |
| HMS-F-003 | Add student details | `students/views.py::add_student`; `students/forms.py::StudentForm`; `students/models.py::Student` | TC-003 | `students/tests.py::StudentViewTest.test_valid_post_creates_student`; `StudentFormTest.test_valid_student_form` | Run #40696524346 | P |
| HMS-F-004 | View student details | `students/views.py::student_detail`; `students/models.py::Student` | TC-004 | `students/tests.py::StudentViewTest.test_admin_can_view_student_detail` | Run #40696524346 | P |
| HMS-F-005 | Update student details | `students/views.py::student_update`; `students/forms.py::StudentForm` | TC-005 | `students/tests.py::StudentViewTest.test_admin_can_update_student`; `test_invalid_update_does_not_save` | Run #40696524346 | P |
| HMS-F-006 | Remove student record | `students/views.py::student_delete`; `students/models.py::Student` | TC-006 | `students/tests.py::StudentViewTest.test_admin_can_delete_student`; `students/test_integration.py` (delete workflow) | Run #40696524346 | P |
| HMS-F-015 | Search student records | `students/views.py::student_list` (Q-filter on usn/name/email/phone/department) | TC-015 | `students/test_functional_search.py::StudentSearchFunctionalTests.test_admin_search_returns_only_matching_student`; `students/tests.py::StudentViewTest.test_search_returns_matching_students` | Run #40696524346 | P |

---

## 2. Functional requirements — Sprint 2 scope (HMS-F-007 to HMS-F-014, HMS-F-016 to HMS-F-017)

Sprint 2 CI evidence: GitHub Actions [run #254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) — functional tests passed.

| Req ID | Requirement | Implementation | STP test case | Actual test identifier | CI evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| HMS-F-007 | Add room details | `rooms/views.py::add_hostel`; `rooms/views.py::add_room`; `rooms/models.py::Hostel`; `rooms/models.py::Room` | TC-007 | `rooms/tests.py::HostelRoomManagementTests.test_admin_can_add_hostel`; `test_admin_can_add_room` | Run #254 | P |
| HMS-F-008 | View available rooms | `rooms/views.py::available_rooms` (filters `occupied_count__lt=capacity`) | TC-008 | `rooms/tests.py::RoomAvailabilityAndDetailsTests.test_available_rooms_include_empty_and_partially_occupied` | Run #254 | P |
| HMS-F-009 | View occupied rooms | `rooms/views.py::occupied_rooms` (filters `occupied_count__gt=0`) | TC-009 | `rooms/tests.py::RoomAvailabilityAndDetailsTests.test_occupied_rooms_include_partially_occupied_and_full` | Run #254 | P |
| HMS-F-010 | Allocate room | `allocations/views.py::allocate_room`; `allocations/services.py::AllocationService.allocate_room`; `allocations/models.py::Allocation` | TC-010 | `allocations/tests.py::AllocationServiceTests.test_successful_room_allocation`; `AllocationPermissionTests.test_admin_can_allocate_room` | Run #254 | P |
| HMS-F-011 | Prevent allocation of a full room | `allocations/services.py::AllocationService.allocate_room` (raises `RoomFullError`); `rooms/services.py::RoomService` | TC-011 | `allocations/tests.py::AllocationServiceTests.test_full_room_rejects_allocation` | Run #254 | P |
| HMS-F-012 | View allocated room | `students/views.py::student_portal_room`; `students/views.py::student_room`; `allocations/models.py::Allocation` | TC-012 | `students/tests.py::StudentPortalTests.test_student_with_active_allocation_can_view_actual_room_details` | Run #254 | P |
| HMS-F-013 | Update room allocation | `allocations/views.py::change_room`; `allocations/services.py::AllocationService.change_room` | TC-013 | `allocations/tests.py::AllocationServiceTests.test_successful_room_change`; `AllocationPermissionTests.test_admin_can_change_student_room` | Run #254 | P |
| HMS-F-014 | Vacate room | `allocations/views.py::vacate_room`; `allocations/services.py::AllocationService.vacate_room` | TC-014 | `allocations/tests.py::AllocationServiceTests.test_successful_room_vacation`; `AllocationPermissionTests.test_admin_can_confirm_room_vacation` | Run #254 | P |
| HMS-F-016 | Update room availability | `rooms/models.py::Room.available_beds` (property); `rooms/services.py::RoomService` (occupancy updates on allocate/change/vacate) | TC-016 | `rooms/tests.py::HostelRoomManagementTests.test_available_beds_calculation`; allocation/change/vacation evidence above (run #254) | Run #254 | P |
| HMS-F-017 | View room details | `rooms/views.py::room_detail`; `rooms/models.py::Room` | TC-017 | `rooms/tests.py::RoomAvailabilityAndDetailsTests.test_room_details_display_correct_information` | Run #254 | P |

---

## 3. Security requirements

Sprint 2 CI evidence: GitHub Actions [run #245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) — all security tests passed.

| Req ID | Requirement | Implementation | STP test case | Actual test identifier | CI evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| HMS-SEC-001 | User authentication | `accounts/views.py::admin_login`; `accounts/middleware.py` (django-axes throttle); `hostel_project/settings.py` (AXES config) | TC-SEC-001 | `accounts/tests.py::AdminAuthenticationTests.test_valid_admin_credentials_allow_login` | Run #245 | P |
| HMS-SEC-002 | Reject invalid credentials | `accounts/views.py::admin_login`; `accounts/forms.py::AdminLoginForm` | TC-SEC-002 | `accounts/tests.py::AdminAuthenticationTests.test_invalid_password_is_rejected`; `test_blank_fields_are_rejected` | Run #245 | P |
| HMS-SEC-003 | Restrict administrator operations | `accounts/views.py::dashboard` (`is_staff` check); `students/views.py` (all views, `is_staff` check); `rooms/views.py` (all views, `is_staff` check); `allocations/views.py` (all views, `is_staff` check) | TC-SEC-003 | `accounts/tests.py::AdminAuthenticationTests.test_non_admin_cannot_access_dashboard`; `students/tests.py::StudentViewTest.test_non_admin_is_forbidden`; `rooms/tests.py::HostelRoomManagementTests.test_non_admin_cannot_access_room_list` | Run #245 | P |
| HMS-SEC-004 | Protect data from unauthorized modification or deletion | Student records: `students/views.py::student_update`, `students/views.py::student_delete` (`is_staff` + CSRF checks). Room records: `rooms/views.py::add_room`, `rooms/views.py::edit_room` (`is_staff` check). Allocation records: `allocations/views.py::allocate_room`, `allocations/views.py::change_room`, `allocations/views.py::vacate_room` (`is_staff` check). Cross-cutting: `hostel_project/settings.py` (CSRF middleware). | TC-SEC-004 | Student: `students/test_security.py::StudentDataProtectionTests.test_non_admin_cannot_update_student`; `test_non_staff_cannot_delete_student`; `test_csrf_token_is_required_for_deletion`. Room: `rooms/test_room_validation.py::RoomValidationTests.test_non_admin_cannot_edit_room`; `rooms/tests.py::HostelRoomManagementTests.test_non_admin_cannot_add_room`. Allocation: `allocations/tests.py::AllocationPermissionTests.test_normal_student_cannot_allocate_room`; `test_normal_student_cannot_change_room`; `test_normal_student_cannot_vacate_room` | Run #245 | P |
| HMS-SEC-005 | Restrict protected access after logout | `accounts/views.py::admin_logout` (`@require_POST`, clears session); `@login_required` on all protected views | TC-SEC-005 | `accounts/tests.py::AdminAuthenticationTests.test_logout_terminates_session`; `test_dashboard_requires_authentication` | Run #245 | P |
| HMS-SEC-006 | Validate input before storage | `students/forms.py::StudentForm` (email, phone, academic_year validators); `rooms/forms.py::RoomForm` (capacity ≥ 1, unique room_number per hostel) | TC-SEC-006 | `students/test_security.py::StudentDataProtectionTests.test_invalid_email_is_not_saved_on_add`; `rooms/test_room_validation.py::RoomValidationTests` | Run #245 | P |

---

## 4. Non-functional requirements

Sprint 2 CI evidence: GitHub Actions [run #270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) — NFR tests passed or assessed with stated limitations.

| Req ID | Requirement | Implementation | STP test case | Actual test identifier | CI evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HMS-NFR-001 | User-friendly interface | `accounts/templates/`; `students/templates/`; `rooms/templates/`; `allocations/templates/` | TC-NFR-001 | `students/test_nonfunctional.py` — primary-interface rendering and heading checks | Run #270 | A | Automated interface smoke check passed. A representative-user usability/accessibility study requires a deployed environment and is outside CI scope. |
| HMS-NFR-002 | Response time within 3 seconds | `students/views.py::student_list`; `accounts/views.py::dashboard`; `rooms/views.py::available_rooms`; `allocations/views.py::allocate_room` | TC-NFR-002 | `students/test_nonfunctional.py::NonFunctionalPerformanceTests.test_normal_admin_operations_meet_response_time_target` | Run #270 | P | All measured in-process MySQL CI operations completed under the enforced 3-second threshold. |
| HMS-NFR-003 | Data accuracy and consistency | `allocations/services.py::AllocationService` (atomic transactions); `allocations/models.py::Allocation` (CheckConstraint); `rooms/services.py::RoomService` | TC-NFR-003 | `students/test_nonfunctional.py` — allocation/vacation consistency check; HOSTEL-41 MySQL integration checks | Run #270 | P | Active allocations and room occupancy remained consistent across tested operations. |
| HMS-NFR-004 | System availability | Django application layer (`manage.py runserver` / WSGI entry point); MySQL database backend (`hostel_project/settings.py` DATABASES config). No production web server, process manager, load balancer, or uptime-monitoring tool is present in this repository. | TC-NFR-004 | `students/test_nonfunctional.py::NonFunctionalPerformanceTests.test_short_run_availability_probe_has_no_failed_requests` — 20-request availability probe | Run #270 | A | All 20 in-process CI probe requests returned HTTP 200 under the threshold. The repository contains no production deployment configuration, no process supervisor, and no uptime-monitoring integration; sustained administrative-hours availability cannot be verified from CI alone. |
| HMS-NFR-005 | Maintainability | Separate Django apps: `accounts/`, `students/`, `rooms/`, `allocations/`; service layer in `rooms/services.py`, `allocations/services.py` | TC-NFR-005 | Full regression suite (`python manage.py test`); separate student, room and allocation module tests | Run #270 | P | Complete automated suite passed; modules remain independently testable. |
| HMS-NFR-006 | Scalability | `students/views.py::student_list` (ORM queryset with Q-filter); `hostel_project/settings.py` (MySQL backend) | TC-NFR-006 | `students/test_nonfunctional.py` — student-list checks at 25, 250 and 500 records | Run #270 | P | Each dataset size returned expected results under the 3-second threshold. Concurrent-load testing remains outside CI scope. |

---

## 5. Acceptance tests

Sprint 2 CI evidence: GitHub Actions [run #280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) — all 16 acceptance tests passed.

Requirement mapping cross-references SRS §6.2 and STP §13. Where a single acceptance test exercises more than one requirement, all linked requirement IDs are listed. Inconsistencies between the SRS, STP §13 and the test reports are noted in the Notes column.

| AT ID | Related requirements | Actual test identifier | CI evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| AT-001 | HMS-F-001; HMS-SEC-001 | `accounts/tests.py::AdminAuthenticationTests.test_valid_admin_credentials_allow_login` | Run #280 | P | SRS §6.2 maps AT-001 to HMS-F-001 (administrator login). STP §13 contains an inconsistency: its traceability matrix maps HMS-F-001 → AT-001 and HMS-SEC-001 → AT-013, but a separate example in STP §13 links both HMS-F-001 and HMS-SEC-001 to AT-001. This RTM follows SRS §6.2 as the authoritative source and includes both IDs. The STP inconsistency is noted here and does not affect test status. |
| AT-002 | HMS-F-002; HMS-SEC-002 | `accounts/tests.py::AdminAuthenticationTests.test_invalid_password_is_rejected` | Run #280 | P | SRS §6.2 maps AT-002 to HMS-F-002 (invalid login handling). STP §13 maps HMS-F-002 → AT-002 and HMS-SEC-002 → AT-002 in its matrix, making them consistent on this row. Both requirement IDs are included here to reflect the full SRS §6.2 and STP §13 coverage. |
| AT-003 | HMS-F-003 | `students/tests.py::StudentViewTest.test_valid_post_creates_student` | Run #280 | P | Consistent. |
| AT-004 | HMS-F-004; HMS-F-015 | `students/tests.py::StudentViewTest.test_admin_can_view_student_detail`; `students/test_functional_search.py::StudentSearchFunctionalTests.test_admin_search_returns_only_matching_student` | Run #280 | P | SRS §6.2 links AT-004 to both HMS-F-004 (view student) and HMS-F-015 (search). The Sprint 2 acceptance RTM listed only HMS-F-005; corrected here to reflect SRS §6.2. |
| AT-005 | HMS-F-005 | `students/tests.py::StudentViewTest.test_admin_can_update_student`; `test_invalid_update_does_not_save` | Run #280 | P | Consistent. |
| AT-006 | HMS-F-007 | `rooms/tests.py::HostelRoomManagementTests.test_admin_can_add_hostel`; `test_admin_can_add_room` | Run #280 | P | Consistent. |
| AT-007 | HMS-F-008 | `rooms/tests.py::RoomAvailabilityAndDetailsTests.test_available_rooms_include_empty_and_partially_occupied` | Run #280 | P | Consistent. |
| AT-008 | HMS-F-010 | `allocations/tests.py::AllocationServiceTests.test_successful_room_allocation` | Run #280 | P | Consistent. |
| AT-009 | HMS-F-011 | `allocations/tests.py::AllocationServiceTests.test_full_room_rejects_allocation` | Run #280 | P | Consistent. |
| AT-010 | HMS-F-012 | `students/tests.py::StudentPortalTests.test_student_with_active_allocation_can_view_actual_room_details` | Run #280 | P | Consistent. |
| AT-011 | HMS-F-013 | `allocations/tests.py::AllocationServiceTests.test_successful_room_change`; `AllocationPermissionTests.test_admin_can_change_student_room` | Run #280 | P | Consistent. |
| AT-012 | HMS-F-014; HMS-F-016 | `allocations/tests.py::AllocationServiceTests.test_successful_room_vacation`; `rooms/tests.py::HostelRoomManagementTests.test_available_beds_calculation` | Run #280 | P | SRS §6.2 links AT-012 to both HMS-F-014 (vacate room) and HMS-F-016 (update room availability). The Sprint 2 acceptance RTM listed only HMS-F-014; corrected here to reflect SRS §6.2. |
| AT-013 | HMS-SEC-001; HMS-SEC-003 | `accounts/tests.py::AdminAuthenticationTests.test_non_admin_cannot_access_dashboard` | Run #280 | P | SRS §6.2 links AT-013 to both HMS-SEC-001 (authentication gate) and HMS-SEC-003 (restrict admin operations). The Sprint 2 acceptance RTM listed only HMS-SEC-003; corrected here to reflect SRS §6.2. |
| AT-014 | HMS-NFR-002 | `students/test_nonfunctional.py::NonFunctionalPerformanceTests.test_normal_admin_operations_meet_response_time_target` | Run #280 | P | Consistent. |
| AT-015 | HMS-NFR-003 | `students/tests.py::StudentViewTest.test_admin_can_update_student`; `test_invalid_update_does_not_save` | Run #280 | P | Consistent. |
| AT-016 | HMS-SEC-005 | `accounts/tests.py::AdminAuthenticationTests.test_logout_terminates_session`; `test_dashboard_requires_authentication` | Run #280 | P | Consistent. |

---

## 6. Not Tested summary

No requirement in this RTM carries NT status. All 17 functional requirements (HMS-F-001 to HMS-F-017), all 6 security requirements (HMS-SEC-001 to HMS-SEC-006), and all 6 non-functional requirements (HMS-NFR-001 to HMS-NFR-006) have automated test evidence recorded against them across the Sprint 1 and Sprint 2 CI runs listed above.

HMS-NFR-001 and HMS-NFR-004 retain **A** (Action Required) status because the automated evidence is an interface smoke check and a short CI availability probe respectively; neither substitutes for a formal human usability study or sustained production uptime monitoring.

---

## 7. Failed and blocked test summary

No test failure or blocked test was recorded in any of the Sprint 1 or Sprint 2 CI runs referenced by this RTM:

| CI run | Tests executed | Passed | Failed | Blocked | Link |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 — run #40696524346 | 61 | 61 | 0 | 0 | [Actions run #40696524346](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346) |
| Security — run #245 | Full suite | All | 0 | 0 | [Actions run #245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) |
| Functional — run #254 | Full suite | All | 0 | 0 | [Actions run #254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) |
| MySQL integration — run #261 | Full suite | All | 0 | 0 | [Actions run #261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521) |
| NFR — run #270 | Full suite | All | 0 | 0 | [Actions run #270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) |
| Acceptance — run #280 | Full suite | All | 0 | 0 | [Actions run #280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) |

No retest was required. No defect ID was raised against any of the above runs.

---

## 8. CI evidence summary

| Activity | Artifact | CI run | Result |
| --- | --- | --- | --- |
| Sprint 1 — authentication and student management | `accounts/tests.py`, `students/tests.py`, `students/test_integration.py`, `students/test_security.py` | [#40696524346](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346) | 61/61 passed |
| Security hardening and TC-SEC-001 to TC-SEC-006 | `docs/HOSTEL-39-security-test-report.md` | [#245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) | Passed |
| Functional room and allocation — TC-007 to TC-017 | `docs/HOSTEL-40-functional-test-report.md` | [#254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) | Passed |
| MySQL integration | `docs/HOSTEL-41-mysql-integration-report.md` | [#261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521) | Passed |
| NFR — TC-NFR-001 to TC-NFR-006 | `docs/HOSTEL-42-non-functional-test-report.md` | [#270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) | Passed / A |
| Acceptance — AT-001 to AT-016 | `docs/HOSTEL-43-acceptance-test-report.md` | [#280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) | 16/16 passed |

---

## 9. Notes

1. P indicates that the listed automated test evidence passed in the referenced CI run.
2. A indicates that automated evidence exists but a stated limitation (usability study, production uptime monitoring) prevents full verification in the CI environment.
3. NT would indicate a requirement with no test evidence; no requirement in this RTM carries NT status.
4. Test identifiers use the format `module/file.py::ClassName.method_name` matching Django's test runner and pytest discovery conventions.
5. AT-001 and AT-002 now include both the SRS §6.2 functional requirement links (HMS-F-001, HMS-F-002) and the security requirement links (HMS-SEC-001, HMS-SEC-002). STP §13 contains an internal inconsistency for AT-001: its matrix maps HMS-F-001 → AT-001 and HMS-SEC-001 → AT-013, while a separate example in §13 links both to AT-001. This RTM follows SRS §6.2 as the authoritative source and documents the STP inconsistency explicitly.
6. AT-004, AT-012 and AT-013 requirement mappings have been corrected against SRS §6.2; the prior Sprint 2 acceptance RTM (`RTM_Sprint2_Acceptance.md`) listed narrower mappings that did not reflect all SRS §6.2 links.
6. Production HTTPS, HSTS, reverse-proxy configuration and external security scanning require verification in the deployed environment as noted in `docs/HOSTEL-38-security-review.md`.
