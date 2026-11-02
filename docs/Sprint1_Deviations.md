# Sprint 1 Deviations and Deferred Scope Record

**Project:** Hostel Management System  
**Team:** 11  
**Sprint:** Sprint 1 (19–23 October 2026)  
**Prepared:** 2 November 2026  
**Baseline documents:** SRS v1.0, SAD v1.0, Software Test Plan v1.0  
**Implementation baseline reviewed:** `main`, including the Sprint 1 demo video merge (PR #16)

## 1. Purpose

This record compares the submitted SRS, SAD and Software Test Plan with the implementation completed for Sprint 1. It distinguishes:

- **Implementation variance:** the implemented configuration differs temporarily from the target stated in the SRS.
- **Planned deferral:** the requirement remains part of the overall system, but the SAD schedules it for a later sprint.
- **Verification pending:** the implementation or quality attribute has not yet been formally verified with the evidence required by the STP.

A requirement marked as deferred or pending must not be described as completed or passed.

## 2. Summary

| Area | Submitted-document baseline | Sprint 1 implementation / evidence | Classification and follow-up |
|---|---|---|---|
| Database | SRS §2.4 and §3.3 specify MySQL. SAD §3.6, ADR-003 identifies MySQL as the target and explicitly allows SQLite for development and CI. | The current Django settings use SQLite. The repository's requirements do not yet configure a MySQL driver or environment-based MySQL connection. | **Temporary implementation variance already acknowledged by the SAD (OI-1).** Add environment-based MySQL settings in the planned database sprint and rerun integration tests against MySQL before release. Do not claim MySQL deployment has been completed. |
| Room management | SRS §2.2 includes hostel/room details, available and occupied rooms, and room availability. | No room-management model/module or working room screens are present in the Sprint 1 code. RTM requirements HMS-F-007 to HMS-F-009 and HMS-F-017 are marked not tested. | **Planned deferral.** SAD §4.6 assigns room management to Sprint 2. Retain as not implemented/not tested until built and verified. |
| Room allocation | SRS §2.2 includes allocate, view, update and vacate room allocation, and prevent allocation of a full room. | No room-allocation module is present in Sprint 1. RTM requirements HMS-F-010 to HMS-F-014 and HMS-F-016 are marked not tested. | **Planned deferral.** SAD §4.6 assigns room allocation to Sprint 2. Capacity and occupancy protections remain unverified until implementation and tests exist. |
| Student portal | SRS §2.3 describes student access to relevant hostel/room information depending on access provided. SAD includes read-only student access in its scope. | No student portal or student-facing login/workspace is present in Sprint 1. | **Planned deferral.** SAD §4.6 assigns the Student Portal to Sprint 2. Confirm demonstration scope with the faculty reviewer as noted in SAD OI-2. |
| Authentication hardening | Security requirements include rejecting invalid credentials and protecting access. SAD also records a limit on repeated failed logins. | The Sprint 1 implementation tests valid/invalid login, blank input, authorization, logout/session behaviour and other student-data protections. A repeated-failed-login rate limit is not implemented. | **Planned security hardening.** SAD OI-3 assigns the repeated-login limit to Sprint 3. Do not claim rate limiting is implemented. |
| HTTPS deployment | SRS §3.4 describes HTTP/HTTPS communication. SAD records the need to document TLS for deployment over a network. | Sprint 1 verification was performed using a local development server; no network HTTPS/TLS deployment evidence is recorded. | **Deployment verification pending.** SAD OI-4 identifies TLS setup as an open issue. Document and verify HTTPS before network deployment. |
| Non-functional requirements | SRS and STP define usability, response-time, data consistency, availability, maintainability and scalability requirements. | RTM records manual UI review and partial student-data consistency evidence. No formal three-second response-time measurement, availability test or load/scalability test is recorded. Formal usability/accessibility evaluation is also pending. | **Verification pending / later-sprint work.** SAD §4.6 schedules performance and scalability testing for Sprint 3. Keep the RTM statuses as Action Required or Not Tested until evidence is recorded. |
| Acceptance and full-system testing | STP includes acceptance tests AT-001 to AT-016 and an overall test exit criterion covering the planned requirements. | Sprint 1 evidence is the 61-test Django suite and successful CI checks for the implemented Sprint 1 scope. There is no evidence in the Sprint 1 RTM that all AT-001 to AT-016 or all room-related tests have passed. | **Full-system acceptance remains pending.** SAD §4.6 schedules acceptance testing and regression testing for Sprint 3. The Sprint 1 test result must not be described as full product acceptance or full STP exit-criteria completion. |

## 3. Items that are not deviations

The following are choices already permitted or explicitly described in the submitted design:

1. **Django instead of Flask:** SRS §2.4 allows Django or Flask. SAD ADR-002 selects Django because of its built-in authentication, sessions, ORM, form validation and CSRF support.
2. **Layered Django application and server-rendered pages:** SAD ADR-001 and ADR-006 select a layered Django MVT application with server-rendered HTML. This remains within the submitted technology choices.
3. **SQLite for Sprint 1 development and CI:** This is not an undocumented database substitution; SAD §3.6 ADR-003 and OI-1 explicitly describe SQLite as development/CI-only and MySQL as the target database. The actual MySQL configuration and verification are still outstanding.
4. **UI refinement:** The login, dashboard and student-management UI redesign (PR #12) improves presentation of the existing Sprint 1 workflows and does not claim to add room or portal functionality.

## 4. Sprint 1 implementation and verification evidence

The Sprint 1 implementation covers administrator authentication and access control, student create/view/update/delete/search workflows, student input validation, security protections for implemented student operations, automated tests, and GitHub Actions CI.

Recorded verification:
- Local `python manage.py check`: passed.
- Local `python manage.py test`: 61 tests run; final result `OK`.
- Test modules: `accounts/tests.py` (8), `students/tests.py` (39), `students/test_integration.py` (5), and `students/test_security.py` (9).
- Latest verified main-branch GitHub Actions run after the demo-video merge: https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/40696524346
- Sprint 1 demo video: `docs/sprint1_demo.mp4`, added through merged PR #16.

These results establish that the implemented Sprint 1 scope passes the recorded checks. They do not establish that the deferred room, allocation, student-portal, MySQL, performance, availability, scalability or full acceptance-test requirements have passed.

## 5. Final-demo explanation

The team can explain the Sprint 1 scope as follows:

> Sprint 1 delivered the authentication, access-control and student-management foundation, with unit, integration and security tests and an automated GitHub Actions pipeline. The SRS describes the complete Hostel Management System, while the submitted SAD phases room management, room allocation, the student portal and MySQL configuration into Sprint 2, and places security hardening, performance/scalability, regression and acceptance testing in Sprint 3. For Sprint 1 development and CI, SQLite is used as a temporary database as expressly documented in SAD ADR-003 and OI-1; MySQL remains the target database and still requires configuration and integration verification before release. We therefore report deferred and unverified requirements as pending, not as completed.

Before presenting this explanation, the team should confirm that the sprint sequencing still matches the latest instruction from the course faculty.

## 6. Outstanding follow-up

- Complete the MySQL configuration and repeat integration tests against MySQL in the sprint assigned by the faculty.
- Implement and test the room-management, room-allocation and student-portal requirements in their planned sprint.
- Complete the deferred security hardening, TLS deployment work, formal NFR measurements, regression and acceptance tests according to the approved schedule.
- Keep the RTM aligned with actual evidence; do not mark untested requirements as Passed.
- The STP §8 also lists test execution logs and a Test Summary Report as test deliverables. The 61-test result and CI links are recorded above; retain the detailed execution evidence and final reviewed test summary in the repository if required by the QA lead/faculty.

## 7. References

- SRS v1.0: `docs/SRS_Hostel_management_system_team11.pdf`
- SAD v1.0: `docs/SAD_Hostel_Management_System_team11.pdf` (especially §3.6 ADR-003, §4.6 OI-1 to OI-4, and the next-steps-by-sprint plan)
- Software Test Plan v1.0: `docs/STP_Hostel_Management_system_team11.pdf` (especially §1.2, §5.3, §8 and §13–14)
- Sprint 1 RTM: `docs/RTM_Sprint1.md`
- CI workflow: `.github/workflows/ci.yml`
