# Hostel Management System — Sprint 2 NFR RTM

Status legend: **P** = Passed, **F** = Failed, **B** = Blocked, **A** = Assessed with stated limitation, **N** = Not executed.

| Requirement ID | Requirement | Test reference | Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| HMS-NFR-001 | User-friendly interface | TC-NFR-001 | Primary-interface rendering and heading checks in `students/test_nonfunctional.py` | Pending | Final status follows HOSTEL-42 CI execution; human usability study remains separate. |
| HMS-NFR-002 | Normal operations respond within 3 seconds | TC-NFR-002 | Timed dashboard, student-list, available-room and allocation-form checks | Pending | Measured in MySQL CI; excludes browser/network latency. |
| HMS-NFR-003 | Accurate and consistent data | TC-NFR-003 | Allocation/vacation consistency test and HOSTEL-41 MySQL checks | Pending | Final status follows HOSTEL-42 CI execution. |
| HMS-NFR-004 | System availability | TC-NFR-004 | 20-request availability probe | Pending | Short CI test window only; full administrative-hours availability needs deployed monitoring. |
| HMS-NFR-005 | Maintainability | TC-NFR-005 | Full regression suite; separate student, room and allocation modules | Pending | Final status follows HOSTEL-42 CI execution. |
| HMS-NFR-006 | Scalability | TC-NFR-006 | Student-list checks at 25, 250 and 500 records | Pending | Basic single-process dataset check; not concurrent load testing. |

