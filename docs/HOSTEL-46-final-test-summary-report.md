# Hostel Management System — Final Software Test Summary Report

## Document Information

- **Jira story:** HOSTEL-46
- **Sprint:** Sprint 2
- **Epic:** Documentation and Final Release
- **Prepared by:** Pavithra G C (QA Lead)
- **GitHub issue:** #58
- **References:** STP Section 5.3, Section 8, Section 14

---

## 1. Purpose

This report consolidates all testing activities carried out during Sprint 1 and Sprint 2 of the Hostel Management System project. It records test execution results, requirement coverage, defect status, response-time measurements and testing limitations, as required by the Software Test Plan.

---

## 2. Test Environment

| Item | Detail |
|---|---|
| CI platform | GitHub Actions (Ubuntu latest) |
| Python version | 3.14 |
| Django version | 5.2.18 |
| Database | MySQL 8.0 (CI service container) |
| Test runner | `python manage.py test` |
| Local OS | Windows (developer machines) |
| Local database (Sprint 1) | SQLite (Django test runner) |
| Local database (Sprint 2) | MySQL 8.0 |

---

## 3. Sprint 1 Test Results

### 3.1 Scope

Sprint 1 covered administrator authentication, student record management (CRUD and search), input validation, student data security, unit and integration tests, and the GitHub Actions CI pipeline.

### 3.2 Test execution

| Test module | Test cases | Passed | Failed | Blocked |
|---|---|---|---|---|
| `accounts/tests.py` — authentication | 8 | 8 | 0 | 0 |
| `students/tests.py` — student management | 39 | 39 | 0 | 0 |
| `students/test_integration.py` — integration | 5 | 5 | 0 | 0 |
| `students/test_security.py` — security | 9 | 9 | 0 | 0 |
| **Sprint 1 total** | **61** | **61** | **0** | **0** |

CI evidence: [GitHub Actions run #40696524346](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346)

### 3.3 Sprint 1 requirement coverage

| Requirement group | Covered | Not tested |
|---|---|---|
| HMS-F-001 to HMS-F-006, HMS-F-015 (authentication and student management) | 7 | 0 |
| HMS-F-007 to HMS-F-014, HMS-F-016, HMS-F-017 (room management and allocation) | 0 | 10 |
| HMS-SEC-001 to HMS-SEC-006 | 6 | 0 |
| HMS-NFR-001 to HMS-NFR-006 | 0 | 6 |

---

## 4. Sprint 2 Test Results

### 4.1 Security Testing (HOSTEL-39)

**CI evidence:** [GitHub Actions run #245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509)

| Test case | Requirement | Result |
|---|---|---|
| TC-SEC-001 — Valid administrator login | HMS-SEC-001 | Passed |
| TC-SEC-002 — Invalid credential rejection | HMS-SEC-002 | Passed |
| TC-SEC-003 — Student blocked from admin pages | HMS-SEC-003 | Passed |
| TC-SEC-004 — Unauthorized modification prevented | HMS-SEC-004 | Passed |
| TC-SEC-005 — Logout terminates session | HMS-SEC-005 | Passed |
| TC-SEC-006 — Input validation before storage | HMS-SEC-006 | Passed |
| Supplemental — Direct URL access blocked | HMS-SEC-003 | Passed |
| Supplemental — Student data isolation | HMS-SEC-004 | Passed |
| Supplemental — SQL injection search | HMS-SEC-006 | Passed |
| Supplemental — XSS output escaping | HMS-SEC-006 | Passed |

| Planned | Executed | Passed | Failed | Blocked |
|---|---|---|---|---|
| 10 | 10 | 10 | 0 | 0 |

### 4.2 Functional Testing — Room Management and Allocation (HOSTEL-40)

**CI evidence:** [GitHub Actions run #254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354)

| Test case | Requirement | Result |
|---|---|---|
| TC-007 — Add hostel and room | HMS-F-007 | Passed |
| TC-008 — List available rooms | HMS-F-008 | Passed |
| TC-009 — List occupied rooms | HMS-F-009 | Passed |
| TC-010 — Allocate room | HMS-F-010 | Passed |
| TC-011 — Prevent full-room allocation | HMS-F-011 | Passed |
| TC-012 — View allocated room | HMS-F-012 | Passed |
| TC-013 — Change room allocation | HMS-F-013 | Passed |
| TC-014 — Vacate room | HMS-F-014 | Passed |
| TC-015 — Student search | HMS-F-015 | Passed |
| TC-016 — Update room availability | HMS-F-016 | Passed |
| TC-017 — View room details | HMS-F-017 | Passed |

| Planned | Executed | Passed | Failed | Blocked |
|---|---|---|---|---|
| 11 | 11 | 11 | 0 | 0 |

### 4.3 MySQL Integration Testing (HOSTEL-41)

**CI evidence:** [GitHub Actions run #261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521)

| Test area | Result |
|---|---|
| MySQL connectivity and backend verification | Passed |
| Migrations and schema verification | Passed |
| Student, hostel, room and allocation persistence | Passed |
| Allocation occupancy consistency | Passed |
| Vacation occupancy release and history retention | Passed |
| Failed-operation rollback without partial records | Passed |
| Foreign-key integrity enforcement | Passed |
| Integrated module operations | Passed |

| Planned | Executed | Passed | Failed | Blocked |
|---|---|---|---|---|
| 8 | 8 | 8 | 0 | 0 |

### 4.4 Non-Functional Testing (HOSTEL-42)

**CI evidence:** [GitHub Actions run #270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695)

| Test case | Requirement | Result | Status |
|---|---|---|---|
| TC-NFR-001 — Usability (interface rendering) | HMS-NFR-001 | Pages rendered with expected headings | Assessed |
| TC-NFR-002 — Response time within 3 seconds | HMS-NFR-002 | All operations under 3-second threshold | Passed |
| TC-NFR-003 — Data accuracy and consistency | HMS-NFR-003 | Allocation and vacation data remained consistent | Passed |
| TC-NFR-004 — System availability probe | HMS-NFR-004 | 20 consecutive requests returned HTTP 200 | Assessed |
| TC-NFR-005 — Maintainability | HMS-NFR-005 | Full regression suite passed | Passed |
| TC-NFR-006 — Scalability (25, 250, 500 records) | HMS-NFR-006 | All dataset sizes returned under threshold | Passed |

| Planned | Executed | Passed | Assessed | Failed | Blocked |
|---|---|---|---|---|---|
| 6 | 6 | 4 | 2 | 0 | 0 |

### 4.5 Acceptance Testing AT-001 to AT-016 (HOSTEL-43)

**CI evidence:** [GitHub Actions run #280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770)

| Test | Requirement | Result |
|---|---|---|
| AT-001 — Administrator login | HMS-F-001; HMS-SEC-001 | Passed |
| AT-002 — Invalid credential rejection | HMS-F-002; HMS-SEC-002 | Passed |
| AT-003 — Student record creation | HMS-F-003 | Passed |
| AT-004 — Student search | HMS-F-004; HMS-F-015 | Passed |
| AT-005 — Student record update | HMS-F-005 | Passed |
| AT-006 — Hostel and room creation | HMS-F-007 | Passed |
| AT-007 — Available room listing | HMS-F-008 | Passed |
| AT-008 — Room allocation | HMS-F-010 | Passed |
| AT-009 — Full-room rejection | HMS-F-011 | Passed |
| AT-010 — Student allocated room view | HMS-F-012 | Passed |
| AT-011 — Room change | HMS-F-013 | Passed |
| AT-012 — Room vacation | HMS-F-014; HMS-F-016 | Passed |
| AT-013 — Unauthorized access denied | HMS-SEC-001; HMS-SEC-003 | Passed |
| AT-014 — Response time target | HMS-NFR-002 | Passed |
| AT-015 — Student update consistency | HMS-NFR-003 | Passed |
| AT-016 — Logout and session termination | HMS-SEC-005 | Passed |

| Planned | Executed | Passed | Failed | Blocked |
|---|---|---|---|---|
| 16 | 16 | 16 | 0 | 0 |

### 4.6 Regression Testing (HOSTEL-44)

**Test module:** `students/test_regression.py`

| Test class | Test methods | Scope |
|---|---|---|
| `AuthenticationRegressionTests` | 3 | Admin login, invalid login, student blocked from dashboard |
| `StudentLifecycleRegressionTests` | 2 | Full student CRUD lifecycle, search |
| `AuthorizationRegressionTests` | 1 | Student blocked from admin pages and mutations |
| `IntegratedRoomAndPortalRegressionTests` | 1 | Room management, allocation, portal, vacation end-to-end |

| Planned | Executed | Passed | Failed | Blocked |
|---|---|---|---|---|
| 7 | 7 | 7 | 0 | 0 |

---

## 5. Consolidated Test Execution Metrics

| Activity | Planned | Executed | Passed | Assessed | Failed | Blocked |
|---|---|---|---|---|---|---|
| Sprint 1 — unit, integration, security | 61 | 61 | 61 | 0 | 0 | 0 |
| Sprint 2 — security testing (HOSTEL-39) | 10 | 10 | 10 | 0 | 0 | 0 |
| Sprint 2 — functional testing (HOSTEL-40) | 11 | 11 | 11 | 0 | 0 | 0 |
| Sprint 2 — MySQL integration (HOSTEL-41) | 8 | 8 | 8 | 0 | 0 | 0 |
| Sprint 2 — non-functional testing (HOSTEL-42) | 6 | 6 | 4 | 2 | 0 | 0 |
| Sprint 2 — acceptance testing (HOSTEL-43) | 16 | 16 | 16 | 0 | 0 | 0 |
| Sprint 2 — regression testing (HOSTEL-44) | 7 | 7 | 7 | 0 | 0 | 0 |
| **Grand total** | **119** | **119** | **117** | **2** | **0** | **0** |

Assessed = automated evidence passed but a stated limitation prevents full verification (TC-NFR-001 usability, TC-NFR-004 availability). These cases are counted as executed and not failed or blocked; they are distinguished from Passed because the STP's full verification intent was not met within the CI environment. See Section 4.4 and Section 9.

---

## 6. Requirement Coverage Summary

| Requirement group | Total | Passed | Action Required | Not Tested |
|---|---|---|---|---|
| Functional — HMS-F-001 to HMS-F-017 | 17 | 17 | 0 | 0 |
| Security — HMS-SEC-001 to HMS-SEC-006 | 6 | 6 | 0 | 0 |
| Non-functional — HMS-NFR-001 to HMS-NFR-006 | 6 | 4 | 2 | 0 |
| **Total** | **29** | **27** | **2** | **0** |

HMS-NFR-001 (usability) and HMS-NFR-004 (availability) are marked Action Required — automated checks passed but formal usability study and sustained uptime monitoring were not conducted. See Section 8.

Full traceability is recorded in `docs/HOSTEL-45-rtm-sprint2-final.md`.

---

## 7. Defect Summary

| Severity | Identified | Resolved | Open |
|---|---|---|---|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 |
| Low | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** |

No defect was identified in the reviewed Sprint 1 and Sprint 2 test artifacts (HOSTEL-39 through HOSTEL-43 reports and the Sprint 1 test execution log).

**Issue-tracker reconciliation is pending.** The HOSTEL-44 QA review (`docs/HOSTEL-44-final-qa-review.md`) records that issue-tracker reconciliation has not been completed and explicitly states: *"current HOSTEL-44 execution and issue-tracker reconciliation remain pending."* The zero-defect counts above reflect the reviewed test artifacts only and cannot be confirmed as final until that reconciliation is complete and any issues found are triaged. Update this table with actual counts once reconciliation is done.

---

## 8. Response-Time Measurements

All figures are individual single-run samples emitted as `NFR_METRIC` log lines by `students/test_nonfunctional.py` in [GitHub Actions run #270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695). They are not averages; no repeated-run average was calculated. The test enforces a hard 3 000 ms threshold per operation and fails automatically if any sample exceeds it.

| Operation | Test method | Sample (ms) | Threshold (ms) | Result |
|---|---|---|---|---|
| Administrator dashboard load | `test_normal_admin_operations_meet_response_time_target` | 3.709 | 3 000 | Passed |
| Student list page load | `test_normal_admin_operations_meet_response_time_target` | 2.098 | 3 000 | Passed |
| Available rooms page load | `test_normal_admin_operations_meet_response_time_target` | 2.542 | 3 000 | Passed |
| Room allocation form load | `test_normal_admin_operations_meet_response_time_target` | 2.752 | 3 000 | Passed |
| Student list — 25 records | `test_student_list_scales_through_500_records` | 3.946 | 3 000 | Passed |
| Student list — 250 records | `test_student_list_scales_through_500_records` | 15.693 | 3 000 | Passed |
| Student list — 500 records | `test_student_list_scales_through_500_records` | 29.468 | 3 000 | Passed |
| Availability probe — max of 20 requests | `test_short_run_availability_probe_has_no_failed_requests` | 2.633 | 3 000 | Passed |

**Note on the previously stated upper bounds.** Earlier versions of this report stated broad upper bounds (e.g. "< 200 ms", "< 500 ms", "< 1 000 ms"). Those figures were not derived from the `NFR_METRIC` log output and have been removed.

**Limitation:** All measurements use the Django test client against a MySQL CI test database. They exclude browser rendering time, external network latency and concurrent-user load. They do not constitute a production performance benchmark.

---

## 9. Testing Limitations and Unresolved Issues

1. GitHub Actions CI verifies the automated test environment only, not a production deployment.
2. Production HTTPS, HSTS and reverse-proxy header behaviour require deployment-specific verification as recorded in HOSTEL-38.
3. HMS-NFR-001 (usability): automated interface rendering checks passed; a formal human usability or accessibility study was not conducted.
4. HMS-NFR-004 (availability): a 20-request CI probe passed; sustained production uptime monitoring was not conducted.
5. Response-time measurements exclude browser rendering, external network latency and representative concurrent-user load.
6. Stakeholder acceptance and production release approval are outside the scope of repository CI.

---

## 10. Exit Criteria Assessment (STP Section 5.3)

| Exit criterion | Status |
|---|---|
| All Sprint 1 and Sprint 2 committed stories implemented and reviewed | Met |
| Functional testing completed — HMS-F-001 to HMS-F-017 | Met |
| Security testing completed — HMS-SEC-001 to HMS-SEC-006 | Met |
| Non-functional testing completed — HMS-NFR-001 to HMS-NFR-006 | Partially met — 4 of 6 cases Passed; HMS-NFR-001 and HMS-NFR-004 remain Action Required (see Section 9) |
| Acceptance tests AT-001 to AT-016 executed and passed | Met — CI run #280 |
| Regression testing completed | Met — 7 regression methods in `students/test_regression.py`; [GitHub Actions run #292](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43678276380) on branch `test/hostel-44-regression-final-qa` |
| No unresolved critical or high-severity defect | Not yet confirmed — issue-tracker reconciliation per HOSTEL-44 QA review is pending (see Section 7) |
| RTM updated and evidence-linked | Met — `docs/HOSTEL-45-rtm-sprint2-final.md` |
| Test summary report prepared and approved (STP §14) | Not yet met — this report is awaiting PR review and approval |
| CI passes on the integrated MySQL build | Latest regression evidence: [GitHub Actions run #292](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43678276380) on branch `test/hostel-44-regression-final-qa`; prior acceptance evidence: CI run #280 |
| Stakeholder acceptance and production release sign-off | Not met — outside CI scope; no sign-off recorded |

**Overall exit status: Conditional — not yet confirmed.**

Automated test evidence is complete and no defect has been identified in the reviewed artifacts. The following items remain open and must be resolved before the exit criteria can be declared fully met:

1. HMS-NFR-001 (usability) and HMS-NFR-004 (availability) remain Action Required; a formal usability study and sustained uptime monitoring have not been conducted.
2. Issue-tracker reconciliation per the HOSTEL-44 QA review is pending; zero open defects cannot be confirmed as final until that is complete.
3. This test summary report is awaiting PR review and approval as required by STP §14.
4. Stakeholder acceptance and production release sign-off are outside CI scope and have not been recorded.

---

## 11. References

| Document | Location |
|---|---|
| Software Test Plan | `docs/STP_Hostel_Management_system_team11.pdf` |
| Sprint 1 RTM | `docs/RTM_Sprint1.md` |
| Sprint 2 Final RTM | `docs/HOSTEL-45-rtm-sprint2-final.md` |
| Sprint 1 Test Execution Log | `docs/Sprint1_Test_Execution_Log.md` |
| Security Test Report | `docs/HOSTEL-39-security-test-report.md` |
| Functional Test Report | `docs/HOSTEL-40-functional-test-report.md` |
| MySQL Integration Report | `docs/HOSTEL-41-mysql-integration-report.md` |
| Non-Functional Test Report | `docs/HOSTEL-42-non-functional-test-report.md` |
| Acceptance Test Report | `docs/HOSTEL-43-acceptance-test-report.md` |
| Regression Test Matrix | `docs/HOSTEL-44-regression-test-matrix.md` |
| Final QA Review | `docs/HOSTEL-44-final-qa-review.md` |
