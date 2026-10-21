# Hostel Management System — Sprint 1 RTM

## Project Information

Project: Hostel Management System
Team: 11
Sprint: Sprint 1
Status legend:
- P = Passed
- N = Not Tested
- A = Action Required

## 1. Functional Requirements

| Requirement ID | Requirement | Test Evidence | Status | Notes |
|---|---|---|---|---|
| HMS-F-001 | Administrator login | accounts/tests.py — valid administrator credentials | P | Automated test passed |
| HMS-F-002 | Invalid login handling | accounts/tests.py — invalid password and blank fields | P | Automated tests passed |
| HMS-F-003 | Add student details | students/tests.py — form validation and student creation | P | Automated tests passed |
| HMS-F-004 | View student details | students/tests.py — administrator student detail test | P | Automated test passed |
| HMS-F-005 | Update student details | students/tests.py — successful and invalid update tests | P | Automated tests passed |
| HMS-F-006 | Remove student record | students/tests.py — deletion tests; students/test_integration.py | P | Automated tests passed |
| HMS-F-007 | Add room details | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-008 | View available rooms | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-009 | View occupied rooms | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-010 | Allocate room | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-011 | Prevent allocation of a full room | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-012 | View allocated room | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-013 | Update room allocation | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-014 | Vacate room | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-015 | Search student records | students/tests.py — search tests | P | Automated tests passed |
| HMS-F-016 | Update room availability | Not implemented in Sprint 1 | N | Planned for Sprint 2 |
| HMS-F-017 | View room details | Not implemented in Sprint 1 | N | Planned for Sprint 2 |

## 2. Security Requirements

| Requirement ID | Requirement | Test Evidence | Status | Notes |
|---|---|---|---|---|
| HMS-SEC-001 | User authentication | accounts/tests.py — valid administrator login | P | Automated test passed |
| HMS-SEC-002 | Reject invalid credentials | accounts/tests.py — invalid password and non-admin login | P | Automated tests passed |
| HMS-SEC-003 | Restrict administrator operations | accounts/tests.py and students/tests.py; students/test_security.py — non-admin and staff permission tests (PR #13) | P | Verified for implemented Sprint 1 functions |
| HMS-SEC-004 | Protect data from unauthorized modification or deletion | students/test_security.py — unauthorized modification and CSRF deletion test | P | Student-management scope tested; room-related scope remains for later |
| HMS-SEC-005 | Restrict protected access after logout | accounts/tests.py — logout session test and authentication checks | P | Automated tests passed |
| HMS-SEC-006 | Validate input before storage | students/tests.py and students/test_security.py — validation tests | P | Student input validation tested; room validation remains for later |

## 3. Non-Functional Requirements

| Requirement ID | Requirement | Evidence | Status | Notes |
|---|---|---|---|---|
| HMS-NFR-001 | User-friendly interface | Manual review of redesigned login, dashboard, and student directory (PR #12) | A | Interface reviewed manually; formal usability/accessibility evaluation still required |
| HMS-NFR-002 | Response time within 3 seconds | No formal timing results recorded | N | Performance measurement pending |
| HMS-NFR-003 | Data accuracy and consistency | Student creation, update, and deletion tests | A | Student scope checked; room/allocation consistency remains for later |
| HMS-NFR-004 | System availability | No formal availability test recorded | N | Verification pending |
| HMS-NFR-005 | Maintainability | Modular Django applications and automated regression tests | A | Formal maintainability evaluation pending |
| HMS-NFR-006 | Scalability | No formal load or scalability results recorded | N | Performance testing pending |

## 4. Overall Sprint 1 Test Evidence

Local configuration check:
python manage.py check — Passed

Local automated test suite:
python manage.py test — 60 tests passed

Continuous Integration:
GitHub Actions workflow completed successfully on main.

Unit and integration test files:
- accounts/tests.py
- students/tests.py
- students/test_integration.py
- students/test_security.py — 8 security tests passed

Relevant pull requests:
- PR #9 — unit and integration tests: https://github.com/SE-TEAM11-HMS/hostel-management-system/pull/9
- PR #10 — student data protection tests: https://github.com/SE-TEAM11-HMS/hostel-management-system/pull/10
- PR #12 — login, dashboard, and student-management UI redesign: https://github.com/SE-TEAM11-HMS/hostel-management-system/pull/12
- PR #13 — staff permission security test: https://github.com/SE-TEAM11-HMS/hostel-management-system/pull/13

CI workflow:
.github/workflows/ci.yml

## 5. Notes

1. Statuses must reflect actual test results.
2. P indicates that the listed test evidence passed.
3. N indicates that the requirement has not yet been tested.
4. A indicates that further verification or action is required.
5. Room management, room allocation, and related requirements remain outside the implemented Sprint 1 scope.
6. Formal test execution records and the final Sprint 1 review must be completed before declaring Sprint 1 closed.