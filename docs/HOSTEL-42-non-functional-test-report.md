# HOSTEL-42 Non-Functional Test Report

## Execution record

- Story: HOSTEL-42 — Execute Non-Functional and Performance Testing
- Test build: `test/hostel-42-nfr-performance`
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0 and Django's MySQL test database.
- Performance target: each representative in-process Django operation must complete within three seconds.
- Current execution state: **Pending the fresh PR CI run.** Measurements and final statuses will be updated from that run.

## NFR test cases

| Test case | Method and workload | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| TC-NFR-001 Usability | Django test client renders the administrator dashboard, student directory, room management and allocation pages; headings provide page context. | Primary pages render successfully with clear headings. | Pending CI execution | Pending |
| TC-NFR-002 Performance | Measure dashboard, student list, available-room list and allocation form responses in the MySQL CI environment. | Each operation is under 3 seconds. | Pending CI execution | Pending |
| TC-NFR-003 Reliability and consistency | Allocate then vacate a room; compare active allocations with room occupancy. | Related data remains consistent. | Pending CI execution | Pending |
| TC-NFR-004 Availability | Issue 20 consecutive authenticated student-list requests in the CI test window. | All requests return HTTP 200 within 3 seconds. | Pending CI execution | Pending |
| TC-NFR-005 Maintainability | Execute the full regression suite and exercise separate student, room and allocation modules through their public views/services. | Modules remain testable and regression checks pass. | Pending CI execution | Pending |
| TC-NFR-006 Scalability | Create and search 25, 250 and 500 student records. | Each measured list request is under 3 seconds and returns the expected count. | Pending CI execution | Pending |

## Observations and limitations

- The availability probe measures a short CI test window only. It does not establish production uptime across an administrative working day because no deployed, monitored environment is available in this repository.
- The usability test is an automated interface smoke check. A formal human usability or accessibility study needs representative users and a deployed test environment.
- The response-time figures are application test-client measurements. They exclude browser rendering, external network latency and concurrent-user load.
- No defect is recorded until the fresh CI execution finishes. Failed cases will be recorded and assigned for correction.

