# HOSTEL-42 Non-Functional Test Report

## Execution record

- Story: HOSTEL-42 — Execute Non-Functional and Performance Testing
- Test build: `test/hostel-42-nfr-performance`
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0 and Django's MySQL test database.
- Performance target: each representative in-process Django operation must complete within three seconds.
- Execution evidence: GitHub Actions [run #270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) passed Django checks, MySQL migrations and the full automated test suite. The test methods emit timing measurements and fail if the three-second threshold is exceeded.

## NFR test cases

| Test case | Method and workload | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| TC-NFR-001 Usability | Django test client renders the administrator dashboard, student directory, room management and allocation pages; headings provide page context. | Primary pages render successfully with clear headings. | All four pages rendered with the expected contextual heading. | Assessed |
| TC-NFR-002 Performance | Measure dashboard, student list, available-room list and allocation form responses in the MySQL CI environment. | Each operation is under 3 seconds. | All four measured operations completed under the 3-second enforced threshold. | Passed |
| TC-NFR-003 Reliability and consistency | Allocate then vacate a room; compare active allocations with room occupancy. | Related data remains consistent. | Allocation increased occupancy, vacation released it and the active-allocation count stayed consistent. | Passed |
| TC-NFR-004 Availability | Issue 20 consecutive authenticated student-list requests in the CI test window. | All requests return HTTP 200 within 3 seconds. | All 20 requests returned HTTP 200 under the 3-second enforced threshold. | Assessed |
| TC-NFR-005 Maintainability | Execute the full regression suite and exercise separate student, room and allocation modules through their public views/services. | Modules remain testable and regression checks pass. | The full suite passed; the NFR checks use the separate module interfaces. | Passed |
| TC-NFR-006 Scalability | Create and search 25, 250 and 500 student records. | Each measured list request is under 3 seconds and returns the expected count. | Each dataset size returned the expected count under the 3-second enforced threshold. | Passed |

## Observations and limitations

- The availability probe measures a short CI test window only. It does not establish production uptime across an administrative working day because no deployed, monitored environment is available in this repository.
- The usability test is an automated interface smoke check. A formal human usability or accessibility study needs representative users and a deployed test environment.
- The response-time figures are application test-client measurements. They exclude browser rendering, external network latency and concurrent-user load.
- No functional or quality defect was identified by this execution. No retest was required.

