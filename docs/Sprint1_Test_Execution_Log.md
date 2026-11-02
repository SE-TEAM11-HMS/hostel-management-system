# Sprint 1 Test Execution Log

**Project:** Hostel Management System  
**Team:** 11  
**Sprint:** Sprint 1 (19–23 October 2026)  
**Execution record prepared:** 2 November 2026  
**Code baseline:** `main` commit `92b8f08c34233c12d7951942b7dbd55326562709` (includes merged Sprint 1 demo video PR #16)

## 1. Purpose and scope

This log records the test execution evidence available for the Sprint 1 implementation. Sprint 1 verification focused on administrator authentication and access control, student record management, input validation, student-data security, unit/integration tests, and the GitHub Actions CI workflow.

The log is not a claim that the full-system exit criteria in the submitted Software Test Plan have been met. Room management, room allocation, MySQL integration, full acceptance testing and formal non-functional testing remain outside the verified Sprint 1 test scope, as recorded in the SAD and RTM.

## 2. Local test execution

**Environment:** Windows development checkout, PowerShell terminal, project virtual environment activated.  
**Database:** Django's configured SQLite database (the test runner creates and destroys its test database).  
**Requirements:** `python -m pip install -r requirements.txt` completed successfully.

| Sequence | Command | Observed result |
|---|---|---|
| 1 | `python manage.py migrate` | Passed; no migrations pending at the time of the run. |
| 2 | `python manage.py check` | Passed; “System check identified no issues (0 silenced).” |
| 3 | `python manage.py test` | Found 61 tests; ran 61 tests in 77.916 seconds; final result `OK`. |

**Execution date:** 28 October 2026. The exact Python patch version and machine specifications were not captured in the screenshot/log available for this record.

## 3. Test distribution by module

| Test module | Test count | Coverage summary |
|---|---:|---|
| `accounts/tests.py` | 8 | Valid and invalid administrator login, blank fields, non-staff login rejection, dashboard authentication/authorization, logout and session termination, GET logout rejection. |
| `students/tests.py` | 39 | Student model and form validation; create, list, detail, update, delete and search; invalid/duplicate data; anonymous and non-staff access restrictions. |
| `students/test_integration.py` | 5 | Login-to-student workflow; add/retrieve, update and delete with database verification; unauthenticated and invalid-input cases. |
| `students/test_security.py` | 9 | Permission boundaries, output escaping, CSRF deletion protection, invalid email/input, injection-like search behaviour, non-staff delete denial, and staff non-superuser access. |
| **Total** | **61** | **All tests in the local run passed.** |

## 4. Continuous integration evidence

The repository's GitHub Actions workflow runs on pushes and pull requests. It installs dependencies, runs `python manage.py check`, and runs `python manage.py test`.

| Evidence | Result |
|---|---|
| Workflow run after Sprint 1 demo video PR #16 merged | Passed |
| Run ID | [40696524346](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346) |
| Branch / commit | `main` / `92b8f08c34233c12d7951942b7dbd55326562709` |
| Job | `Django Checks and Tests` — success |

The successful CI run verifies that the configured Django check and automated test job completed successfully on this commit.

## 5. Scope not verified by this Sprint 1 execution

The following remain unverified and must not be reported as passed:

- Room creation, room availability, occupied-room views and room details (RTM HMS-F-007 to HMS-F-009 and HMS-F-017).
- Room allocation, full-room protection, viewing/updating allocations, vacating rooms and room availability updates (RTM HMS-F-010 to HMS-F-014 and HMS-F-016).
- MySQL integration tests. Sprint 1 local development and CI use SQLite; the SAD records MySQL configuration and MySQL integration verification as later work.
- Formal response-time measurement against the three-second target, availability testing, load/scalability testing, and formal usability/accessibility evaluation.
- Full acceptance-test execution AT-001 to AT-016 and the broader release-level STP exit criteria.

The current RTM records the relevant room and non-functional requirements as Not Tested or Action Required. Their statuses should only be changed when the corresponding evidence exists.

## 6. Defect and sign-off note

No separate defect-report artifact or formal QA/faculty sign-off record was found in the repository's `docs/` folder at the time this log was prepared. The QA lead and team should confirm the defect status and any required approvals before stating that the STP's final release sign-off criteria are satisfied.

## 7. References

- [Sprint 1 RTM](RTM_Sprint1.md)
- [SRS v1.0](SRS_Hostel_management_system_team11.pdf)
- [SAD v1.0](SAD_Hostel_Management_System_team11.pdf)
- [Software Test Plan v1.0](STP_Hostel_Management_system_team11.pdf)
- [GitHub Actions CI run 40696524346](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346)
- [Sprint 1 demo video](sprint1_demo.mp4)
