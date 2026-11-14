# Hostel Management System — Sprint 2 NFR RTM

Status legend: **P** = Passed, **F** = Failed, **B** = Blocked, **A** = Assessed with stated limitation, **N** = Not executed.

| Requirement ID | Requirement | Test reference | Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| HMS-NFR-001 | User-friendly interface | TC-NFR-001 | Primary-interface rendering and heading checks in `students/test_nonfunctional.py`; CI run #270 | A | Automated interface evidence passed. A representative-user usability/accessibility study remains outside the CI environment. |
| HMS-NFR-002 | Normal operations respond within 3 seconds | TC-NFR-002 | Timed dashboard, student-list, available-room and allocation-form checks; CI run #270 | P | All representative MySQL CI operations were under the enforced three-second threshold. |
| HMS-NFR-003 | Accurate and consistent data | TC-NFR-003 | Allocation/vacation consistency test and HOSTEL-41 MySQL checks; CI run #270 | P | Active allocations and room occupancy remained consistent. |
| HMS-NFR-004 | System availability | TC-NFR-004 | 20-request availability probe; CI run #270 | A | All probe requests passed under the threshold. Full administrative-hours availability needs deployed monitoring. |
| HMS-NFR-005 | Maintainability | TC-NFR-005 | Full regression suite and separate student, room and allocation module tests; CI run #270 | P | The complete automated suite passed. |
| HMS-NFR-006 | Scalability | TC-NFR-006 | Student-list checks at 25, 250 and 500 records; CI run #270 | P | Each tested dataset returned expected results under the threshold; concurrent-load testing remains outside this check. |

