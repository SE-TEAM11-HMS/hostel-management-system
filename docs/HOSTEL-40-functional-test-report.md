# HOSTEL-40 Functional Test Report

## Execution record

- Story: HOSTEL-40 — Execute Functional Tests for Room Management and Allocation
- Test build: `test/hostel-40-functional-evidence`
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0 and the Django test database.
- Evidence standard: A case is marked **Passed** only when its listed automated evidence completes successfully in the PR's GitHub Actions run. A case is **Failed** when expected and actual behaviour differ, and **Blocked** when it cannot be run.
- Execution evidence: GitHub Actions [run #254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) completed successfully, including Django configuration checks, migrations and the full automated test suite.

## Functional test cases

| Test case | Requirement | Expected result | Automated evidence | Actual result | Status |
| --- | --- | --- | --- | --- | --- |
| TC-007 | HMS-F-007: create hostels and rooms | Valid hostel and room data is persisted with the entered details. | `rooms.tests.HostelRoomManagementTests.test_admin_can_add_hostel`; `test_admin_can_add_room` | Hostel and room were created with the supplied values. | Passed |
| TC-008 | HMS-F-008: list available rooms | Empty and partly occupied rooms are listed; full rooms are excluded. | `rooms.tests.RoomAvailabilityAndDetailsTests.test_available_rooms_include_empty_and_partially_occupied` | Empty and partly occupied rooms were listed; the full room was excluded. | Passed |
| TC-009 | HMS-F-009: list occupied rooms | Partly and fully occupied rooms are listed; empty rooms are excluded. | `rooms.tests.RoomAvailabilityAndDetailsTests.test_occupied_rooms_include_partially_occupied_and_full` | Partly and fully occupied rooms were listed; the empty room was excluded. | Passed |
| TC-010 | HMS-F-010: allocate an available room | An active allocation is created and the room occupancy increases. | `allocations.tests.AllocationServiceTests.test_successful_room_allocation`; `AllocationPermissionTests.test_admin_can_allocate_room` | An active allocation was created and occupancy increased. | Passed |
| TC-011 | HMS-F-011: prevent full-room allocation | Allocation is rejected, occupancy remains at capacity and no active allocation is created. | `allocations.tests.AllocationServiceTests.test_full_room_rejects_allocation` | Allocation was rejected; occupancy stayed at capacity and no active allocation was created. | Passed |
| TC-012 | HMS-F-012: display an allocated room | The linked student sees the allocated hostel and room information. | `students.tests.StudentPortalTests.test_student_with_active_allocation_can_view_actual_room_details` | The student portal displayed the linked student's hostel and room details. | Passed |
| TC-013 | HMS-F-013: change an allocation | The old allocation is vacated, a new active allocation is created and both room occupancies update. | `allocations.tests.AllocationServiceTests.test_successful_room_change`; `AllocationPermissionTests.test_admin_can_change_student_room` | The old allocation was vacated, the new allocation was active and occupancy values updated. | Passed |
| TC-014 | HMS-F-014: vacate an allocation | The allocation is marked vacated and capacity is released. | `allocations.tests.AllocationServiceTests.test_successful_room_vacation` | The allocation was vacated and room occupancy returned to zero. | Passed |
| TC-015 | Student record search | An administrator searching by a student identifier sees the matching record and not unrelated records. | `students.test_functional_search.StudentSearchFunctionalTests.test_admin_search_returns_only_matching_student` | The matching student was returned and the unrelated student was excluded. | Passed |
| TC-016 | HMS-F-016: maintain room availability | Allocation, room change and vacation keep occupancy and available-bed values consistent. | Allocation, change and vacation evidence above; `rooms.tests.HostelRoomManagementTests.test_available_beds_calculation` | Occupancy and available-bed values remained consistent across the tested operations. | Passed |
| TC-017 | HMS-F-017: view room details | The detail page shows the selected room's hostel, capacity, occupancy and available beds. | `rooms.tests.RoomAvailabilityAndDetailsTests.test_room_details_display_correct_information` | The page showed the selected room's matching hostel, capacity, occupancy and available-bed data. | Passed |

## Defect record and retesting

No functional defect was identified by this execution. No retest was required.

## Scope limit

This is automated integration-test evidence for the application's MySQL CI environment. It does not claim a separate production deployment test.
