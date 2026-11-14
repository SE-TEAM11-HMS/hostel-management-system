# HOSTEL-43 Acceptance Test Execution Report

## Execution record

- Story: HOSTEL-43 — Execute Acceptance Tests AT-001 to AT-016
- Test build: `test/hostel-43-acceptance-evidence`
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0 and Django's MySQL test database.
- Evidence standard: A case is marked **Passed** only after its listed automated evidence completes in this PR's GitHub Actions run. A case is **Failed** for an observed mismatch and **Blocked** if it cannot execute.
- Current execution state: **Pending the fresh PR CI run.** The matrix will be finalized from that run.

## Acceptance test matrix

| Test | Expected result | Automated execution evidence | Actual result | Status |
| --- | --- | --- | --- | --- |
| AT-001 Valid administrator login | Valid administrator credentials create a session and open the dashboard. | `accounts.tests.AdminAuthenticationTests.test_valid_admin_credentials_allow_login` | Pending CI execution | Pending |
| AT-002 Invalid login credentials | Invalid credentials are rejected without creating a session. | `test_invalid_password_is_rejected` | Pending CI execution | Pending |
| AT-003 Add student | Valid details create a student record. | `students.tests.StudentViewTest.test_valid_post_creates_student` | Pending CI execution | Pending |
| AT-004 Search student | A search returns the matching record and excludes unrelated records. | `students.test_functional_search.StudentSearchFunctionalTests.test_admin_search_returns_only_matching_student` | Pending CI execution | Pending |
| AT-005 Update student | Valid updates persist to the selected student. | `students.tests.StudentViewTest.test_admin_can_update_student` | Pending CI execution | Pending |
| AT-006 Add hostel room | Valid hostel and room details are stored. | `rooms.tests.HostelRoomManagementTests.test_admin_can_add_hostel`; `test_admin_can_add_room` | Pending CI execution | Pending |
| AT-007 View available rooms | Available rooms include empty/partial rooms and exclude full rooms. | `rooms.tests.RoomAvailabilityAndDetailsTests.test_available_rooms_include_empty_and_partially_occupied` | Pending CI execution | Pending |
| AT-008 Allocate available room | A valid allocation is active and increments occupancy. | `allocations.tests.AllocationServiceTests.test_successful_room_allocation` | Pending CI execution | Pending |
| AT-009 Allocate full room | Allocation is rejected with no partial record or occupancy change. | `test_full_room_rejects_allocation` | Pending CI execution | Pending |
| AT-010 View allocated room | The linked student sees the correct active hostel and room. | `students.tests.StudentPortalTests.test_student_with_active_allocation_can_view_actual_room_details` | Pending CI execution | Pending |
| AT-011 Change allocation | The old allocation is vacated and the new room becomes active. | `allocations.tests.AllocationServiceTests.test_successful_room_change` | Pending CI execution | Pending |
| AT-012 Vacate allocation | Allocation history is retained and occupancy is released. | `test_successful_room_vacation` | Pending CI execution | Pending |
| AT-013 Unauthorized administrative access | A non-administrator receives HTTP 403 for an administrator page. | `accounts.tests.AdminAuthenticationTests.test_non_admin_cannot_access_dashboard` | Pending CI execution | Pending |
| AT-014 Response time | Representative normal operations complete under the 3-second CI threshold. | `students.test_nonfunctional.NonFunctionalPerformanceTests.test_normal_admin_operations_meet_response_time_target` | Pending CI execution | Pending |
| AT-015 Modify student consistency | A valid edit persists; an invalid edit does not partially overwrite existing data. | `students.tests.StudentViewTest.test_admin_can_update_student`; `test_invalid_update_does_not_save` | Pending CI execution | Pending |
| AT-016 Logout protected page | Logout clears the session and the protected dashboard requires re-authentication. | `accounts.tests.AdminAuthenticationTests.test_logout_terminates_session`; `test_dashboard_requires_authentication` | Pending CI execution | Pending |

## Defect and retest record

No defect is recorded until the fresh CI execution completes. A failed case will be entered here with the observed result, linked defect, correction and retest outcome.

## Scope limit

This provides automated acceptance evidence for the integrated MySQL CI build. Production deployment, network latency and manual stakeholder sign-off are outside this repository-based execution.
