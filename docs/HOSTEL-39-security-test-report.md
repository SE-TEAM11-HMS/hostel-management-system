# HOSTEL-39 Security Test Report

## Test execution record

- Story: HOSTEL-39 — Execute Security Test Cases
- Scope: TC-SEC-001 through TC-SEC-006, with direct-URL, SQL-injection and cross-site-scripting checks recorded as supplemental coverage.
- Test build: `security/hostel-38-hardening` at `755e9b2`.
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0, Django test database.
- Evidence: GitHub Actions run [#245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) completed successfully. It ran Django configuration checks, migrations and the full automated test suite.
- Result terminology: **Passed** means the automated test's expected security behaviour was observed. **Failed** means an observed mismatch. **Blocked** means the check could not be executed.

## Planned security test cases

| Test case | Security objective | Evidence executed in the suite | Result |
| --- | --- | --- | --- |
| TC-SEC-001 | Valid administrator credentials provide authorized access. | `accounts.tests.AdminAuthenticationTests.test_valid_admin_credentials_allow_login` verifies login redirects to the dashboard and creates an authenticated session. | Passed |
| TC-SEC-002 | Invalid credentials are rejected without a session. | `test_invalid_password_is_rejected` and `test_blank_fields_are_rejected` verify generic rejection and required-field validation. | Passed |
| TC-SEC-003 | Students cannot access administrator operations. | `test_non_admin_cannot_access_dashboard`, student-management protection tests, and room-management protection tests verify HTTP 403 and no unauthorized changes. | Passed |
| TC-SEC-004 | Unauthorized modification and deletion are prevented. | `students.test_security.StudentDataProtectionTests.test_non_admin_cannot_update_student`, `test_non_staff_cannot_delete_student`, and `test_csrf_token_is_required_for_deletion` verify data remains unchanged. | Passed |
| TC-SEC-005 | Logout terminates the session and protected pages require authentication again. | `accounts.tests.AdminAuthenticationTests.test_logout_terminates_session` verifies the session is cleared; protected-page tests verify an unauthenticated request redirects to login. | Passed |
| TC-SEC-006 | Invalid student and room input is rejected server-side. | Student invalid-email tests and `rooms.test_room_validation.RoomValidationTests` verify invalid fields, capacities and duplicates are rejected without partial saves. | Passed |

## Supplemental security checks

| Check | Evidence executed in the suite | Result |
| --- | --- | --- |
| Direct URL access | Admin dashboard, student-management, and room-management tests request protected URLs as a non-staff user and expect HTTP 403. | Passed |
| Student data isolation | The student portal resolves the record from the authenticated user and does not use a request-supplied student ID; existing portal access tests exercise that authenticated route. | Passed |
| Basic SQL injection | `students.test_security.StudentDataProtectionTests.test_injection_like_search_does_not_return_all_students` submits `' OR '1'='1` and verifies unrelated records are not returned. | Passed |
| Basic cross-site scripting | `students.test_security.StudentDataProtectionTests.test_student_name_is_escaped_on_detail_page` stores a script-like name and verifies it is not rendered as executable HTML. | Passed |

## Defects and retesting

No defects were identified by this execution. No retest was required.

## Limits and follow-up

These results are automated integration-test evidence for the application code and database. Production HTTPS, HSTS and reverse-proxy header behaviour require verification in the deployed environment, as recorded in HOSTEL-38. This report must be re-run if the security-sensitive views, forms or authentication flow change.
