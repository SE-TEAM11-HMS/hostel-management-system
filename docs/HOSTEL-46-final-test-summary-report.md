# Hostel Management System — Final Software Test Summary Report

**Jira story:** HOSTEL-46  
**Sprint:** Sprint 2  
**Epic:** Documentation & Final Release  
**Prepared by:** Pavithra G C  
**GitHub issue:** #58  
**Report date:** Sprint 2 completion

---

## 1. Purpose

This report consolidates all test execution evidence from Sprint 1 and Sprint 2 of the Hostel Management System project. It records planned and executed test counts, requirement coverage, defect status, performance results, and known limitations.

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

---

## 3. Sprint 1 Test Results

### 3.1 Test activities

| Activity | Test file(s) | Tests executed | Passed | Failed | Skipped |
|---|---|---|---|---|---|
| Authentication unit tests | `accounts/tests.py` | 10 | 10 | 0 | 0 |
| Student management unit tests | `students/tests.py` | 35 | 35 | 0 | 0 |
| Integration tests | `students/test_integration.py` | 8 | 8 | 0 | 0 |
| Security / data-protection tests | `students/test_security.py` | 9 | 9 | 0 | 0 |
| **Sprint 1 total** | | **62** | **62** | **0** | **0** |

CI evidence: [GitHub Actions run #39745586188](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/39745586188)

### 3.2 Sprint 1 requirement coverage

- HMS-F-001 to HMS-F-006, HMS-F-015: Passed
- HMS-F-007 to HMS-F-014, HMS-F-016, HMS-F-017: Not tested (planned for Sprint 2)
- HMS-SEC-001 to HMS-SEC-006: Passed
- HMS-NFR-001 to HMS-NFR-006: Partially assessed or not tested

---

## 4. Sprint 2 Test Results

### 4.1 Security testing (HOSTEL-39)

| Test area | Tests | Passed | CI run |
|---|---|---|---|
| Authentication and invalid login | 4 | 4 | [#245](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/42785878509) |
| Access restrictions (admin vs student) | 6 | 6 | #245 |
| Protected mutations (delete, allocate) | 4 | 4 | #245 |
| Logout and session termination | 2 | 2 | #245 |
| Input validation and injection checks | 4 | 4 | #245 |
| **Security total** | **20** | **20** | |

### 4.2 Functional room and allocation testing (HOSTEL-40)

| Test area | Tests | Passed | CI run |
|---|---|---|---|
| Room creation and listing | 5 | 5 | [#254](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43616388354) |
| Available and occupied room views | 4 | 4 | #254 |
| Room allocation and full-room prevention | 6 | 6 | #254 |
| Room change and vacation | 4 | 4 | #254 |
| Student search and room details | 4 | 4 | #254 |
| **Functional total** | **23** | **23** | |

### 4.3 MySQL integration testing (HOSTEL-41)

| Test area | Tests | Passed | CI run |
|---|---|---|---|
| MySQL backend and migrations | 3 | 3 | [#261](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43618572521) |
| Allocation persistence and consistency | 4 | 4 | #261 |
| Transaction rollback | 2 | 2 | #261 |
| Foreign-key enforcement | 2 | 2 | #261 |
| **MySQL integration total** | **11** | **11** | |

### 4.4 Non-functional testing (HOSTEL-42)

| Test area | Tests | Passed | CI run | Limitation |
|---|---|---|---|---|
| Response-time probe (test-client) | 3 | 3 | [#270](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43620655695) | Test-client only; excludes browser/network |
| Availability probe | 1 | 1 | #270 | Short probe; not sustained uptime |
| **NFR total** | **4** | **4** | | |

### 4.5 Acceptance testing (HOSTEL-43)

| Test area | Tests (AT-001 to AT-016) | Passed | CI run |
|---|---|---|---|
| Authentication and access control | AT-001, AT-002, AT-013, AT-016 | 4 | [#280](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43623547770) |
| Student management | AT-003, AT-004, AT-005 | 3 | #280 |
| Room and allocation | AT-006 to AT-012 | 7 | #280 |
| Non-functional | AT-014, AT-015 | 2 | #280 |
| **Acceptance total** | **16** | **16** | |

### 4.6 Regression testing (HOSTEL-44)

| Test class | Methods | Scope |
|---|---|---|
| `AuthenticationRegressionTests` | 3 | Admin login, invalid login, student blocked from dashboard |
| `StudentLifecycleRegressionTests` | 2 | Full student CRUD lifecycle, search |
| `AuthorizationRegressionTests` | 1 | Student blocked from admin pages and mutations |
| `IntegratedRoomAndPortalRegressionTests` | 1 | Room management, allocation, portal, vacation end-to-end |
| **Regression total** | **7** | |

---

## 5. Consolidated Test Counts

| Category | Planned | Executed | Passed | Failed | Skipped / Blocked |
|---|---|---|---|---|---|
| Sprint 1 (unit, integration, security) | 62 | 62 | 62 | 0 | 0 |
| Sprint 2 security (HOSTEL-39) | 20 | 20 | 20 | 0 | 0 |
| Sprint 2 functional (HOSTEL-40) | 23 | 23 | 23 | 0 | 0 |
| Sprint 2 MySQL integration (HOSTEL-41) | 11 | 11 | 11 | 0 | 0 |
| Sprint 2 NFR (HOSTEL-42) | 4 | 4 | 4 | 0 | 0 |
| Sprint 2 acceptance (HOSTEL-43) | 16 | 16 | 16 | 0 | 0 |
| Sprint 2 regression (HOSTEL-44) | 7 | 7 | 7 | 0 | 0 |
| **Grand total** | **143** | **143** | **143** | **0** | **0** |

---

## 6. Requirement Coverage Summary

| Requirement group | Total | Passed | Not Tested | Failed / Blocked |
|---|---|---|---|---|
| Functional (HMS-F-001 to HMS-F-017) | 17 | 17 | 0 | 0 |
| Security (HMS-SEC-001 to HMS-SEC-006) | 6 | 6 | 0 | 0 |
| Non-functional (HMS-NFR-001 to HMS-NFR-006) | 6 | 4 (assessed) | 2 | 0 |
| **Total** | **29** | **27** | **2** | **0** |

HMS-NFR-001 (usability) and HMS-NFR-006 (scalability) were not formally tested; see Section 8.

---

## 7. Defect Summary

| Severity | Open | Resolved | Total |
|---|---|---|---|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 |
| Low | 0 | 0 | 0 |

No defect was recorded in any Sprint 1 or Sprint 2 test activity. This reflects the reviewed test artifacts only.

---

## 8. Measured Performance Results

| Operation | Method | Measured time | Threshold | Result |
|---|---|---|---|---|
| Student list page load | Django test client | < 200 ms | 3 000 ms | Pass |
| Student detail page load | Django test client | < 200 ms | 3 000 ms | Pass |
| Room allocation POST | Django test client | < 300 ms | 3 000 ms | Pass |

**Limitation:** These measurements use the Django test client against an in-memory test database. They exclude browser rendering time, external network latency, and concurrent-user load. They do not constitute a production performance benchmark.

---

## 9. Test Limitations and Deviations

1. GitHub Actions CI verifies the automated test environment, not a production deployment.
2. Production HTTPS, HSTS, reverse-proxy configuration and external security scanning require deployment-specific verification (noted in HOSTEL-38/39).
3. The short availability probe in HOSTEL-42 does not establish sustained production uptime.
4. Test-client response times do not include browser rendering, external network latency or representative concurrent-user load.
5. HMS-NFR-001 (usability) was assessed by manual template review only; no formal accessibility or usability study was conducted.
6. HMS-NFR-006 (scalability) was not tested; formal load testing is out of scope for this academic project.
7. Stakeholder acceptance and production release approval are outside the scope of repository CI.

---

## 10. Updated RTM Reference

The full Requirements Traceability Matrix covering all Sprint 1 and Sprint 2 requirements is maintained in:

`docs/HOSTEL-45-rtm-sprint2-final.md`

---

## 11. Exit Criteria Assessment (STP §5.3)

| Exit criterion | Status |
|---|---|
| All committed Sprint 2 stories implemented and reviewed | Met |
| Functional, security, NFR, regression and acceptance tests executed | Met |
| No unresolved critical or high-severity defect | Met |
| RTM updated and evidence-linked | Met (HOSTEL-45) |
| SAD updated to reflect final implementation | Met (HOSTEL-47) |
| README accurate and reproducible | Met (HOSTEL-48) |
| CI passes on the integrated MySQL build | Met (CI run #280) |

**Overall exit status: Passed** — subject to the limitations documented in Section 9.
