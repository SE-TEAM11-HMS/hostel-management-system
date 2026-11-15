# HOSTEL-44 Regression Test Matrix

## Execution record

- Story: HOSTEL-44 — Perform Regression Testing and Final QA Review
- GitHub issue: #56
- Test build: `test/hostel-44-regression-final-qa`
- Environment: GitHub Actions CI configured for Ubuntu, Python 3.14, MySQL 8.0 and Django's MySQL test database.
- Execution status: **Pending the pull request's fresh CI run.** Do not change a case to Passed until the corresponding test has completed successfully on this branch.
- Automated entry point: `python manage.py test`
- New focused regression module: `students.test_regression`

## Regression test matrix

| ID | Requirement / risk | Regression procedure and expected result | Automated evidence | Current status |
| --- | --- | --- | --- | --- |
| REG-001 | HMS-F-001; HMS-SEC-001 — administrator authentication | Submit valid administrator credentials; verify dashboard access and authenticated session. | `AuthenticationRegressionTests.test_admin_can_authenticate_and_open_dashboard` | Pending CI |
| REG-002 | HMS-SEC-002 — invalid login handling | Submit an incorrect password; verify generic rejection and no authenticated session. | `AuthenticationRegressionTests.test_invalid_credentials_do_not_create_an_authenticated_session` | Pending CI |
| REG-003 | HMS-SEC-003 — administrative access restrictions | Verify a student account receives HTTP 403 for administrator dashboard, student records and room-management pages. | `AuthenticationRegressionTests.test_student_account_remains_blocked_from_admin_dashboard`; `AuthorizationRegressionTests.test_student_cannot_access_or_mutate_admin_student_and_room_records` | Pending CI |
| REG-004 | HMS-F-002 to HMS-F-006 — student record lifecycle | Create a student, view the detail page, update fields, delete by POST and verify the record no longer exists. | `StudentLifecycleRegressionTests.test_student_create_view_update_and_delete_lifecycle` | Pending CI |
| REG-005 | HMS-F-001 to HMS-F-006 — student search | Search by USN and verify only the matching student appears. | `StudentLifecycleRegressionTests.test_student_search_returns_matching_record_without_unrelated_records` | Pending CI |
| REG-006 | HMS-SEC-004 to HMS-SEC-006 — protected data and mutation | Attempt student deletion and room allocation as a student; verify HTTP 403 and no database mutation. | `AuthorizationRegressionTests.test_student_cannot_access_or_mutate_admin_student_and_room_records` | Pending CI |
| REG-007 | HMS-F-007 to HMS-F-009 — Room Management | Verify room list, available-room list and room detail remain accessible to an administrator after integration. | `IntegratedRoomAndPortalRegressionTests.test_room_management_allocation_student_portal_and_vacation_work_together` | Pending CI |
| REG-008 | HMS-F-010 to HMS-F-016 — Room Allocation | Allocate a room, verify active allocation and occupancy increment, then vacate and verify occupancy release and history retention. | `IntegratedRoomAndPortalRegressionTests.test_room_management_allocation_student_portal_and_vacation_work_together` | Pending CI |
| REG-009 | HMS-F-012; HMS-F-017 — Student Portal | Verify the authenticated linked student sees their own active hostel and room after allocation. | `IntegratedRoomAndPortalRegressionTests.test_room_management_allocation_student_portal_and_vacation_work_together` | Pending CI |
| REG-010 | Defect-fix regression | Re-run the complete test suite after any correction; retain the failed result and link the corrected test to its retest run. | Full `python manage.py test` CI job and linked defect/retest record | Pending CI / as needed |

## Prior evidence reviewed

| Activity | Artifact reviewed | Evidence reference |
| --- | --- | --- |
| Security testing | `docs/HOSTEL-39-security-test-report.md` | [GitHub Actions run #245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) |
| Functional room/allocation testing | `docs/HOSTEL-40-functional-test-report.md` | [GitHub Actions run #254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) |
| MySQL integration and consistency | `docs/HOSTEL-41-mysql-integration-report.md` | [GitHub Actions run #261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521) |
| NFR and performance checks | `docs/HOSTEL-42-non-functional-test-report.md` | [GitHub Actions run #270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) |
| Acceptance tests AT-001 to AT-016 | `docs/HOSTEL-43-acceptance-test-report.md` | [GitHub Actions run #280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) |
| Consolidated Sprint 2 results | `docs/Sprint2_Test_Summary_Report.md` | Previous integrated CI evidence and documented release limitations |

## Defect and retest log

No critical or high-severity defect is listed in the reviewed HOSTEL-39 through HOSTEL-43 reports. This is a statement about those artifacts only; it is not proof that the current regression run has no defects.

| Defect ID | Severity | Affected test | Correction / linked PR | Retest run | Status |
| --- | --- | --- | --- | --- | --- |
| None recorded in the reviewed evidence | — | — | — | — | No prior defect recorded; current regression run pending |

If a regression test fails, record a defect ID, severity, affected requirement, reproduction steps, expected and actual behaviour, owner, correction PR, and the fresh retest run before marking it resolved.

## Metrics to finalize from CI

| Metric | Value |
| --- | --- |
| Regression cases defined in this matrix | 10 |
| New automated regression methods | 7 |
| Full-suite tests executed on this PR | Pending CI |
| Passed / failed / skipped tests | Pending CI |
| Critical / high / medium / low defects | Pending review and CI |
| Retests required / passed | Pending CI and defect triage |

Do not infer the full-suite pass count from the number of new tests. Use the actual GitHub Actions output for final metrics.
