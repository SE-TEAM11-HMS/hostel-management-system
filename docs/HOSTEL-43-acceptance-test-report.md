# HOSTEL-43 Acceptance Test Execution Report

## Execution record

- Story: HOSTEL-43 — Execute Acceptance Tests AT-001 to AT-016
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0 and Django's MySQL test database.
- Evidence: GitHub Actions [run #280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) passed Django checks, MySQL migrations and the full automated suite.

## Acceptance test matrix

| Test | Expected result | Automated execution evidence | Actual result | Status |
| --- | --- | --- | --- | --- |
| AT-001 | Valid administrator credentials open the dashboard. | `AdminAuthenticationTests.test_valid_admin_credentials_allow_login` | Session created and dashboard redirect completed. | Passed |
| AT-002 | Invalid credentials are rejected. | `test_invalid_password_is_rejected` | Rejected without a session. | Passed |
| AT-003 | Valid student details create a record. | `StudentViewTest.test_valid_post_creates_student` | Record created. | Passed |
| AT-004 | Search finds the matching student only. | `StudentSearchFunctionalTests.test_admin_search_returns_only_matching_student` | Matching record returned; unrelated record excluded. | Passed |
| AT-005 | Valid student updates persist. | `StudentViewTest.test_admin_can_update_student` | Updated values persisted. | Passed |
| AT-006 | Valid hostel and room details are stored. | `HostelRoomManagementTests.test_admin_can_add_hostel`; `test_admin_can_add_room` | Hostel and room created. | Passed |
| AT-007 | Available rooms exclude full rooms. | `RoomAvailabilityAndDetailsTests.test_available_rooms_include_empty_and_partially_occupied` | Correct rooms listed. | Passed |
| AT-008 | Available-room allocation is active and increments occupancy. | `AllocationServiceTests.test_successful_room_allocation` | Active allocation and occupancy update recorded. | Passed |
| AT-009 | Full-room allocation is rejected without partial change. | `test_full_room_rejects_allocation` | Rejected with no allocation created. | Passed |
| AT-010 | Student sees their allocated room. | `StudentPortalTests.test_student_with_active_allocation_can_view_actual_room_details` | Correct hostel and room displayed. | Passed |
| AT-011 | Room change vacates old allocation and activates new room. | `AllocationServiceTests.test_successful_room_change` | Allocation and occupancy values updated. | Passed |
| AT-012 | Vacation releases occupancy and retains history. | `test_successful_room_vacation` | Allocation marked vacated and capacity released. | Passed |
| AT-013 | Unauthorized admin access is denied. | `AdminAuthenticationTests.test_non_admin_cannot_access_dashboard` | HTTP 403 returned. | Passed |
| AT-014 | Normal operations meet the three-second target. | `NonFunctionalPerformanceTests.test_normal_admin_operations_meet_response_time_target` | All measured operations were under the enforced threshold. | Passed |
| AT-015 | Student edit remains consistent. | `StudentViewTest.test_admin_can_update_student`; `test_invalid_update_does_not_save` | Valid edit persisted; invalid edit caused no partial overwrite. | Passed |
| AT-016 | Logout clears session and protected page needs login. | `AdminAuthenticationTests.test_logout_terminates_session`; `test_dashboard_requires_authentication` | Session cleared; dashboard redirected to login. | Passed |

## Defect and retest record

No acceptance defect was identified. No retest was required.

## Scope limit

This is automated acceptance evidence for the integrated MySQL CI build. Production deployment validation, network latency and stakeholder sign-off remain separate release activities.
