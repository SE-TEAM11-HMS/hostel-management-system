# Unit and System Test Report

**Project:** Hostel Management System
**Report date:** 16 November 2026
**Verified branch commit:** `098d1eec39a793e35d8c1cd04f43ebe2b7f1a39b` (`test: measure and publish Django code coverage`)
**CI run:** [Hostel Management System CI — run 43807823551](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43807823551)

## 1. Summary

The new unit and end-to-end system test modules passed as part of the complete MySQL-backed Django test run. GitHub Actions reported **205 tests run, all passing**. Coverage measurement for the application modules reported **91.77% combined line-and-branch coverage**.

| Measure | Result |
|---|---:|
| Unit tests in the new standalone unit module | 4 passed |
| New end-to-end system workflow test | 1 passed |
| Full repository test suite in CI | 205 passed, 0 failed |
| Coverage scope | `accounts`, `students`, `rooms`, `allocations` |
| Coverage result | 91.77% combined line-and-branch coverage |

The full-suite run completed in 67.896 seconds. Django system checks, migrations, and coverage artifact upload also succeeded.

## 2. Unit test report

**File:** [`rooms/test_unit.py`](../rooms/test_unit.py)
**Test type:** Isolated model behavior using Django `SimpleTestCase`; these tests do not require a database.

| Test case | Expected behavior | Result |
|---|---|---|
| Hostel string representation | Includes hostel name and block | Passed |
| Available-bed calculation | Capacity minus occupied beds | Passed |
| Full-room availability | Returns zero available beds when full | Passed |
| Room string representation | Includes hostel and room number | Passed |

**Standalone result:** 4 tests passed locally; the same tests were included in the CI suite.

## 3. System test report

**File:** [`students/test_system.py`](../students/test_system.py)
**Test type:** Database-backed end-to-end workflow using Django's test client and the configured MySQL test database.

The workflow exercises the public application routes in sequence:

1. Administrator authenticates and opens the dashboard and room views.
2. Administrator allocates a room to a student.
3. The linked student authenticates through the student login and views the profile and room page.
4. Administrator changes the student's room.
5. Student portal displays the changed room.
6. Administrator vacates the allocation; room occupancy is released and allocation history remains.

**Result:** Passed in the full MySQL-backed CI run. No failed or blocked tests were reported.

## 4. Code coverage

Coverage is measured by `coverage.py` with branch tracking enabled. The configured source scope is the four application packages (`accounts`, `students`, `rooms`, and `allocations`). Test files and migrations are excluded from the source coverage calculation.

| Coverage metric | Result |
|---|---:|
| Application statements measured | 652 |
| Statements missed | 45 |
| Branches measured | 150 |
| Partial branches | 17 |
| Combined line-and-branch coverage | **91.77%** |

The CI workflow generates `coverage.xml` and an HTML coverage report, then uploads them as the **`django-test-coverage`** artifact attached to the [successful CI run](https://github.com/SE-TEAM11-HMS/hostel-management-system/actions/runs/43807823551).

To reproduce coverage locally, install the development requirements and run:

```powershell
pip install -r requirements-dev.txt
coverage run manage.py test
coverage report -m
coverage xml
coverage html
```

The HTML report is written to `htmlcov/index.html`. Database-backed tests require a working local MySQL setup and the project's local `.env` configuration.

## 5. CI evidence and limitations

The verified GitHub Actions run used MySQL 8.0, applied migrations, ran the full Django test suite under coverage, and uploaded the coverage reports successfully. The coverage percentage describes Python statements and branches in the four listed application packages; it is not a percentage for templates, database-engine internals, or external systems. Coverage indicates which code paths were exercised, not a guarantee that every possible input or production environment has been tested.
