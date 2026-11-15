# Hostel Management System — Software Architecture and Design Specification

## Document Information

- **Document title:** Software Architecture and Design Specification
- **Version:** 2.0 (Sprint 2 Final)
- **Jira story:** HOSTEL-47
- **Sprint:** Sprint 2
- **Epic:** Documentation and Final Release
- **Prepared by:** Prabhakar Kumar
- **GitHub issue:** #59
- **Supersedes:** SAD v1.0 (`docs/SAD_Hostel_Management_System_team11.pdf`)

---

## 1. Introduction

### 1.1 Purpose

This document describes the software architecture and design of the Hostel Management System (HMS) as implemented at the end of Sprint 2. It revises SAD v1.0 to reflect the completed application, documents all implemented modules, records implementation deviations from the original design, and corrects all sprint-plan references to the actual two-sprint development plan.

### 1.2 Scope

The HMS is a Django web application that allows hostel administrators to manage student records, hostel and room information, and room allocations. Students access a read-only self-service portal to view their own profile and allocated room. The system uses MySQL as its database.

### 1.3 Intended audience

- Development team members
- QA lead and testers
- Faculty reviewer and evaluators

### 1.4 References

- SRS v1.0 — `docs/SRS_Hostel_management_system_team11.pdf`
- STP v1.0 — `docs/STP_Hostel_Management_system_team11.pdf`
- SAD v1.0 — `docs/SAD_Hostel_Management_System_team11.pdf`
- Sprint 1 Deviations Record — `docs/Sprint1_Deviations.md`
- Security Review — `docs/HOSTEL-38-security-review.md`

---

## 2. Development Plan

The project was completed in exactly **two sprints**. All references to a three-sprint plan in SAD v1.0 are superseded by this document.

| Sprint | Dates | Scope |
|---|---|---|
| Sprint 1 | 19–23 October 2026 | Administrator authentication, student record management (CRUD and search), unit tests, integration tests, security tests, GitHub Actions CI pipeline |
| Sprint 2 | 2–4 November 2026 | MySQL configuration, room management, room allocation, student portal, security hardening, functional/NFR/acceptance/regression testing, documentation |

Items previously assigned to a Sprint 3 in SAD v1.0 (security hardening, performance testing, acceptance testing) were completed in Sprint 2.

---

## 3. Architectural Overview

The HMS follows the standard **Django MTV (Model–Template–View)** pattern deployed as a single-server web application.

```
Browser
  │
  ▼
Django URL Router  (hostel_project/urls.py)
  │
  ├── accounts app     — login, logout, dashboard, middleware
  ├── students app     — student CRUD, search, student portal
  ├── rooms app        — hostel/room creation, listing, detail
  └── allocations app  — allocate, change, vacate room
  │
  ▼
MySQL 8.0 Database  (hostel_db)
```

### 3.1 Technology stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.11 or newer (CI: 3.14) |
| Web framework | Django | 5.2.18 |
| Database | MySQL | 8.0 |
| Database driver | mysqlclient | 2.3.0 |
| Brute-force protection | django-axes | 9.0.0 |
| Environment configuration | python-dotenv | 1.2.4 |
| CI platform | GitHub Actions | Ubuntu latest |

### 3.2 Deployment environments

| Environment | Database | Notes |
|---|---|---|
| Local development | MySQL 8.0 via `.env` | Credentials in `.env`; never committed |
| CI (GitHub Actions) | MySQL 8.0 service container | Credentials in workflow environment variables |
| Production | MySQL 8.0 | HTTPS, HSTS and reverse-proxy configuration required |

**Deviation from SAD v1.0:** SAD v1.0 (ADR-003, OI-1) allowed SQLite for Sprint 1 development and CI. Sprint 2 completed the MySQL configuration. All environments now use MySQL. SQLite is no longer used.

---

## 4. Module Descriptions

### 4.1 accounts — Authentication and Access Control

**Responsibility:** Administrator and student login, logout, dashboard access, session management, and no-cache response headers.

| Component | Description |
|---|---|
| `views.py` — `LoginView` | Validates administrator credentials. Uses `django-axes` for brute-force protection (5 attempts per username/IP in a rolling 15-minute window; returns HTTP 429 on lockout). Redirects to dashboard on success. |
| `views.py` — `StudentLoginView` | Separate login endpoint for student accounts. Redirects to `student_portal` on success. |
| `views.py` — `LogoutView` | POST-only. Clears the session and redirects to the login page. |
| `views.py` — `DashboardView` | Requires authentication and `is_staff=True`. Returns HTTP 403 for non-staff users. |
| `middleware.py` — `AuthenticatedNoCacheMiddleware` | Adds `Cache-Control: no-store` to all authenticated responses to prevent back-button access after logout. |
| `forms.py` | Login form with username and password fields. |

**Service interface:** All views accept standard Django HTTP requests. Authentication state is maintained via Django's session framework.

---

### 4.2 students — Student Record Management and Student Portal

**Responsibility:** CRUD operations on student records (administrator), student search, student portal (student read-only view), and student–user account association.

#### 4.2.1 Administrator student management

| Component | Description |
|---|---|
| `models.py` — `Student` | Fields: `usn` (unique), `name`, `email` (unique), `phone` (10-digit regex), `department`, `academic_year` (1–4), `user` (FK to `AUTH_USER_MODEL`, nullable). |
| `views.py` — `StudentListView` | Staff-only. Supports `?q=` search across USN, name, email, phone and department (case-insensitive). |
| `views.py` — `StudentCreateView` | Staff-only. Validates via `StudentForm`. Displays success message on creation. |
| `views.py` — `StudentDetailView` | Staff-only. Returns HTTP 404 for non-existent student. |
| `views.py` — `StudentUpdateView` | Staff-only. Validates via `StudentForm`. Displays success message on update. |
| `views.py` — `StudentDeleteView` | Staff-only. POST-only (GET returns HTTP 405). Redirects to student list on success. |
| `views.py` — `StudentRoomView` | Staff-only. Displays the active allocation for a given student. |
| `forms.py` — `StudentForm` | Validates phone (10 digits), academic year (1–4) and all required fields. |

#### 4.2.2 Student Portal

**New in Sprint 2.** Deviation from SAD v1.0: the student portal was listed as deferred scope in OI-2. It is now fully implemented.

| Component | Description |
|---|---|
| `views.py` — `StudentPortalView` | Login-required (student). Resolves the student record from the authenticated user. Ignores any `student_id` query parameter (IDOR prevention). Returns HTTP 403 for unlinked accounts. |
| `views.py` — `StudentPortalRoomView` | Login-required (student). Displays the student's own active room allocation. |
| `portal_urls.py` | URL patterns for student portal endpoints. |

**Access control rule:** A student user must have a linked `Student` record (`student.user == request.user`). Unlinked accounts receive HTTP 403. Students cannot access any administrator page (HTTP 403).

---

### 4.3 rooms — Room Management

**New in Sprint 2.** Responsibility: hostel and room creation, listing (all, available, occupied), room detail, and room editing.

| Component | Description |
|---|---|
| `models.py` — `Hostel` | Fields: `name` (unique), `block`. |
| `models.py` — `Room` | Fields: `hostel` (FK, CASCADE), `room_number`, `capacity` (≥ 1), `occupied_count` (0 ≤ x ≤ capacity). Property: `available_beds = capacity − occupied_count`. Unique constraint: `(hostel, room_number)`. |
| `views.py` — `AddHostelView` | Staff-only. Creates a new hostel. |
| `views.py` — `AddRoomView` | Staff-only. Creates a room under a hostel. |
| `views.py` — `RoomListView` | Staff-only. Lists all rooms. |
| `views.py` — `AvailableRoomsView` | Staff-only. Lists rooms where `available_beds > 0`. |
| `views.py` — `OccupiedRoomsView` | Staff-only. Lists rooms where `occupied_count > 0`. |
| `views.py` — `RoomDetailView` | Staff-only. Shows room details and current allocations. |
| `views.py` — `EditRoomView` | Staff-only. Updates room capacity. |
| `services.py` — `RoomService` | Business logic for room validation. |
| `forms.py` | Room creation and edit forms. |

**Database integrity rules:**
- `capacity ≥ 1` (CheckConstraint)
- `0 ≤ occupied_count ≤ capacity` (CheckConstraint)
- `(hostel, room_number)` unique per hostel (UniqueConstraint)

---

### 4.4 allocations — Room Allocation

**New in Sprint 2.** Responsibility: allocating a room to a student, changing allocation, vacating a room, and maintaining `occupied_count` consistency.

| Component | Description |
|---|---|
| `models.py` — `Allocation` | Fields: `student` (FK, PROTECT), `room` (FK, PROTECT), `active_student` (FK, nullable, unique — enforces one active allocation per student in MySQL), `allocated_at`, `vacated_at`, `status` (ACTIVE / VACATED). |
| `services.py` — `AllocationService.allocate_room` | Checks room capacity. Creates `Allocation`. Increments `room.occupied_count`. Wrapped in a database transaction. |
| `services.py` — `AllocationService.change_room` | Vacates the current allocation. Creates a new allocation in the new room. Atomic transaction. |
| `services.py` — `AllocationService.vacate_room` | Sets `status = VACATED` and `vacated_at = now()`. Decrements `room.occupied_count`. Retains allocation history. |
| `views.py` — `AllocateRoomView` | Staff-only POST. Calls `AllocationService.allocate_room`. |
| `views.py` — `ChangeRoomView` | Staff-only. Calls `AllocationService.change_room`. |
| `views.py` — `VacateRoomView` | Staff-only POST with confirmation. Calls `AllocationService.vacate_room`. |

**Database integrity rules:**
- `unique_active_allocation_per_student` (UniqueConstraint on `active_student`) — a student cannot have two active allocations simultaneously. MySQL allows multiple NULL values in a unique column, enabling multiple vacated records per student.
- `allocation_status_vacated_at_consistent` (CheckConstraint) — `ACTIVE` ↔ `vacated_at IS NULL`; `VACATED` ↔ `vacated_at IS NOT NULL`.
- `Allocation.save()` sets `active_student = student` when ACTIVE and `NULL` when VACATED.

**Deviation from SAD v1.0:** The `active_student` field was not described in SAD v1.0. It was added to enforce the one-active-allocation-per-student rule using MySQL's unique constraint behaviour with nullable columns.

---

## 5. Database Design

### 5.1 MySQL configuration

| Setting | Value | Source |
|---|---|---|
| Engine | `django.db.backends.mysql` | `hostel_project/settings.py` |
| Database name | `hostel_db` | `.env` — `DB_NAME` |
| User | `hostel_app` | `.env` — `DB_USER` |
| Password | (not committed) | `.env` — `DB_PASSWORD` |
| Host | `127.0.0.1` | `.env` — `DB_HOST` |
| Port | `3306` | `.env` — `DB_PORT` |
| Charset | `utf8mb4` | `settings.py` OPTIONS |

All credentials are read from `.env` via `python-dotenv`. No credential is committed to source code. `.env` is listed in `.gitignore`.

**Deviation from SAD v1.0:** SAD v1.0 (ADR-003, OI-1) described MySQL as the target database with SQLite as a temporary development/CI substitute. Sprint 2 completed the MySQL configuration. MySQL is now used in all environments.

### 5.2 Entity–Relationship summary

```
User (Django built-in)
  │ 1
  │ N
Student ──────────────── Allocation ──────────────── Room
  (usn, name, email,       (student FK,                (hostel FK,
   phone, department,       room FK,                    room_number,
   academic_year,           active_student FK nullable, capacity,
   user FK nullable)        status,                     occupied_count)
                            allocated_at,
                            vacated_at)
                                                            │ N
                                                            │ 1
                                                         Hostel
                                                         (name, block)
```

### 5.3 Key database constraints

| Table | Constraint | Type |
|---|---|---|
| `students_student` | `usn` unique | UNIQUE |
| `students_student` | `email` unique | UNIQUE |
| `students_student` | `academic_year` between 1 and 4 | CHECK |
| `students_student` | `phone` exactly 10 digits | CHECK + validator |
| `rooms_room` | `(hostel_id, room_number)` unique | UNIQUE |
| `rooms_room` | `capacity ≥ 1` | CHECK |
| `rooms_room` | `0 ≤ occupied_count ≤ capacity` | CHECK |
| `allocations_allocation` | `active_student` unique (nullable) | UNIQUE |
| `allocations_allocation` | status consistent with vacated_at | CHECK |

---

## 6. Security Architecture

| Control | Implementation | Status |
|---|---|---|
| Authentication | Django built-in auth; passwords hashed with PBKDF2 | Implemented |
| Brute-force protection | `django-axes` — 5 failures per username/IP in 15-minute window; HTTP 429 on lockout | Implemented (Sprint 2) |
| Session security | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE=Lax` | Implemented |
| CSRF protection | `CsrfViewMiddleware`; all state-changing views use POST with CSRF token; logout is POST-only | Implemented |
| No-cache headers | `AuthenticatedNoCacheMiddleware` adds `Cache-Control: no-store` to authenticated responses | Implemented (Sprint 2) |
| Clickjacking prevention | `X_FRAME_OPTIONS=DENY` | Implemented |
| Content-type sniffing | `SECURE_CONTENT_TYPE_NOSNIFF=True` | Implemented |
| Referrer policy | `SECURE_REFERRER_POLICY=same-origin` | Implemented |
| Authorization | `is_staff` check on every administrator view; HTTP 403 for non-staff | Implemented |
| Student data isolation | Portal resolves student from authenticated user; ignores request-supplied student ID | Implemented (Sprint 2) |
| Input validation | Django form validators + model `CheckConstraint` + model `clean()` | Implemented |
| No secrets in source | All secrets in `.env`; `.env` is git-ignored | Implemented |
| HTTPS (production) | `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS` configurable via `.env` | Configurable; disabled for local HTTP development |

**Deviation from SAD v1.0:** SAD v1.0 (OI-3) deferred repeated-login rate limiting to Sprint 3. `django-axes` was implemented in Sprint 2 (HOSTEL-38).

---

## 7. API and Service Interfaces

### 7.1 URL structure

| URL pattern | App | Access |
|---|---|---|
| `/login/` | accounts | Public |
| `/student-login/` | accounts | Public |
| `/logout/` | accounts | Authenticated (POST only) |
| `/dashboard/` | accounts | Staff only |
| `/students/` | students | Staff only |
| `/students/add/` | students | Staff only |
| `/students/<pk>/` | students | Staff only |
| `/students/<pk>/update/` | students | Staff only |
| `/students/<pk>/delete/` | students | Staff only |
| `/students/<pk>/room/` | students | Staff only |
| `/portal/` | students | Student only |
| `/portal/room/` | students | Student only |
| `/hostels/add/` | rooms | Staff only |
| `/rooms/` | rooms | Staff only |
| `/rooms/add/` | rooms | Staff only |
| `/rooms/available/` | rooms | Staff only |
| `/rooms/occupied/` | rooms | Staff only |
| `/rooms/<pk>/` | rooms | Staff only |
| `/rooms/<pk>/edit/` | rooms | Staff only |
| `/allocations/allocate/` | allocations | Staff only |
| `/allocations/change/` | allocations | Staff only |
| `/allocations/<pk>/vacate/` | allocations | Staff only |

### 7.2 Service layer

The `AllocationService` in `allocations/services.py` encapsulates all allocation business logic. Views call service methods rather than manipulating models directly. All service operations that modify multiple records run inside a database transaction.

---

## 8. Implementation Deviations from SAD v1.0

| Area | SAD v1.0 description | Final implementation | Status |
|---|---|---|---|
| Database | SQLite for development/CI (ADR-003, OI-1); MySQL as target | MySQL used in all environments (local, CI, production) | Resolved in Sprint 2 |
| Sprint plan | Three sprints described | Project completed in two sprints; Sprint 3 items moved to Sprint 2 | Resolved |
| Student portal | Deferred to Sprint 2 (OI-2) | Fully implemented in Sprint 2 (HOSTEL-33 to HOSTEL-37) | Resolved |
| Brute-force login protection | Deferred to Sprint 3 (OI-3) | `django-axes` implemented in Sprint 2 (HOSTEL-38) | Resolved |
| `active_student` field | Not described in SAD v1.0 | Added to `Allocation` model to enforce one-active-allocation-per-student via MySQL unique constraint | Addition |
| `AuthenticatedNoCacheMiddleware` | Not described in SAD v1.0 | Added to prevent back-button access after logout | Addition |
| Service layer (`AllocationService`, `RoomService`) | Not described in SAD v1.0 | Added to separate business logic from views | Addition |

---

## 9. Open Issues

| Issue ID | Description | Status |
|---|---|---|
| OI-1 | MySQL configuration (originally SQLite for development) | Resolved — MySQL configured in Sprint 2 |
| OI-2 | Student portal scope confirmation | Resolved — fully implemented in Sprint 2 |
| OI-3 | Repeated-login rate limiting | Resolved — `django-axes` implemented in Sprint 2 |
| OI-4 | HTTPS/TLS deployment verification | Open — requires deployment-specific configuration; outside repository CI scope |
| OI-5 | Formal usability/accessibility evaluation (HMS-NFR-001) | Open — manual review only; formal study deferred as future work |
| OI-6 | Formal load/scalability testing (HMS-NFR-006) | Open — dataset-size scaling verified; concurrent-load testing deferred as future work |

---

## 10. Future Work (Out of Scope)

- Production HTTPS/TLS deployment and HSTS configuration
- Formal human usability and accessibility study
- Concurrent-user load testing
- Fee and fine management
- Mess management
- Multi-hostel deployment
- Email and SMS notifications
- Report export
