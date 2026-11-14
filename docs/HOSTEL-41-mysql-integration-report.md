# HOSTEL-41 MySQL Integration and Data Consistency Report

## Execution record

- Story: HOSTEL-41 — Verify MySQL Integration and Data Consistency
- Test build: `test/hostel-41-mysql-integration`
- Environment: GitHub Actions, Ubuntu, Python 3.14, MySQL 8.0 and Django's MySQL test database.
- Evidence standard: A result is **Passed** only after the listed automated evidence completes in this PR's GitHub Actions run. **Failed** records an observed mismatch; **Blocked** records an unexecutable case.
- Current execution state: **Pending the fresh PR CI run.** This report will be finalized from the resulting run.

## Database integration test cases

| Area | Expected result | Evidence | Actual result | Status |
| --- | --- | --- | --- | --- |
| MySQL connectivity | Django uses the MySQL backend and can execute a database query. | `MySQLIntegrationAndConsistencyTests.test_uses_mysql_and_migrated_application_tables` | Pending CI execution | Pending |
| Migrations and schema | Migrations apply before tests and core student, hostel, room and allocation tables exist. | CI `Apply database migrations` step; `test_uses_mysql_and_migrated_application_tables` | Pending CI execution | Pending |
| Persistence and retrieval | Student, hostel, room and allocation records persist and retrieve with matching related records. | `test_student_hostel_room_and_allocation_persist_and_retrieve` | Pending CI execution | Pending |
| Allocation consistency | Allocation increments room occupancy; active allocation count equals `occupied_count`. | `test_active_allocations_match_room_occupancy_after_allocation` | Pending CI execution | Pending |
| Vacation consistency | Vacation marks the allocation vacated, releases occupancy and preserves history. | `test_vacation_releases_occupancy_and_preserves_history` | Pending CI execution | Pending |
| Failed-operation rollback | A full-room allocation raises an error without creating an active allocation or changing occupancy. | `test_failed_allocation_rolls_back_without_partial_records` | Pending CI execution | Pending |
| Foreign-key integrity | MySQL rejects an allocation with a nonexistent student reference. | `test_database_foreign_key_rejects_invalid_allocation_reference` | Pending CI execution | Pending |
| Integrated modules | Student, room and allocation models operate together through the allocation service in MySQL. | Persistence, allocation and vacation tests above | Pending CI execution | Pending |

## Defects and retesting

No defect is recorded until the fresh CI execution completes. A failed case will be documented with the observed result, assigned for correction and re-executed after the correction.

## Scope limit

This verifies the repository's MySQL CI integration and its application-level database operations. It does not claim production database availability, backup/restore testing or performance/load testing.
