# Hostel Management System — Software Architecture and Design Specification (SAD)

**Version:** 2.0 (Sprint 2 final)  
**Jira story:** HOSTEL-47  
**Sprint:** Sprint 2  
**Epic:** Documentation & Final Release  
**Prepared by:** Prabhakar Kumar  
**GitHub issue:** #59  
**Supersedes:** SAD v1.0

---

## 1. Introduction

### 1.1 Purpose

This document describes the software architecture and design of the Hostel Management System (HMS) as implemented at the end of Sprint 2. It reconciles the original SAD v1.0 with the final codebase and records implementation deviations.

### 1.2 Scope

The HMS is a Django web application that allows hostel administrators to manage student records, hostel and room information, and room allocations. Students access a read-only portal to view their own profile and allocated room. The system uses MySQL as its database.

### 1.3 Project plan

The project was completed in exactly **two sprints**:

| Sprint | Scope |
|---|---|
| Sprint 1 | Administrator authentication, student record management (CRUD + search), unit/integration/security tests, CI pipeline |
| Sprint 2 | MySQL configuration, room management, room allocation, student portal, security hardening, full test suite, documentation |

There is no Sprint 3. All Sprint 3 references in earlier drafts are superseded by this document.

---

## 2. Architectural Overview

The HMS follows a standard **Django MTV (Model–Template–View)** architecture deployed as a single-server web application.

```
Browser
  │
  ▼
Django URL router  (hostel_project/urls.py)
  │
  ├── accounts app   — login, logout, dashboard
  ├── students app   — student CRUD, search, student portal
  ├── rooms app      — hostel/room creation, listing, detail
  └── allocations app — allocate, change, vacate room
  │
  ▼
MySQL 8.0 database  (hostel_db)
```

### 2.1 Technology stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.11+ (CI: 3.14) |
| Web framework | Django | 5.2.18 |
| Database | MySQL | 8.0 |
| Database driver | mysqlclient | 2.3.0 |
| Authentication | Django built-in auth + django-axes | 9.0.0 |
| Session management | Django sessions (database-backed) | — |
| Environment config | python-dotenv | 1.2.4 |
| CI | GitHub Actions | — |

### 2.2 Deployment environment

- **Development:** Local machine, SQLite or MySQL via `.env`
- **CI:** GitHub Actions, Ubuntu, MySQL 8.0 service container
- **Production:** Single server with MySQL; HTTPS termination via reverse proxy (deployment-specific)

---

## 3. Module Descriptions

### 3.1 `accounts` — Authentication and Access Control

**Responsibility:** Administrator and student login, logout, dashboard, and session management.

**Key components:**

| Component | Description |
|---|---|
| `views.py` — `LoginView` | Validates credentials; uses `django-axes` for brute-force protection (5 attempts / 15 min). Redirects admin to dashboard, student to portal. |
| `views.py` — `StudentLoginView` | Separate login endpoint for student accounts; redirects to `student_portal`. |
| `views.py` — `LogoutView` | POST-only; clears session and redirects to login. |
| `views.py` — `DashboardView` | Staff-only (`is_staff=True`); returns HTTP 403 for non-staff. |
| `middleware.py` — `AuthenticatedNoCacheMiddleware` | Adds `Cache-Control: no-store` for authenticated responses to prevent back-button access after logout. |
| `forms.py` | Login form with username and password fields. |

**Security controls:**
- `django-axes` locks out after 5 failed attempts per username+IP for 15 minutes.
- `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = "Lax"`.
- `CSRF_COOKIE_HTTPONLY = True`.
- `X_FRAME_OPTIONS = "DENY"`, `SECURE_CONTENT_TYPE_NOSNIFF = True`.

---

### 3.2 `students` — Student Record Management and Portal

**Responsibility:** CRUD operations on student records (admin), student search, student portal (read-only student view), and student–user account association.

**Key components:**

| Component | Description |
|---|---|
| `models.py` — `Student` | Fields: `usn` (unique), `name`, `email` (unique), `phone` (10-digit regex), `department`, `academic_year` (1–4), `user` (FK to `AUTH_USER_MODEL`, nullable). |
| `views.py` — `StudentListView` | Staff-only; supports `?q=` search across USN, name, email, phone, department (case-insensitive). |
| `views.py` — `StudentCreateView` | Staff-only; validates via `StudentForm`; shows success message. |
| `views.py` — `StudentDetailView` | Staff-only; 404 for non-existent student. |
| `views.py` — `StudentUpdateView` | Staff-only; validates via `StudentForm`; shows success message. |
| `views.py` — `StudentDeleteView` | Staff-only; POST-only (GET returns 405); redirects to list. |
| `views.py` — `StudentRoomView` | Staff-only; shows active allocation for a student. |
| `views.py` — `StudentPortalView` | Login-required (student); shows own profile and active allocation. Ignores `student_id` query parameter (IDOR prevention). |
| `views.py` — `StudentPortalRoomView` | Login-required (student); shows own active room allocation. |
| `forms.py` — `StudentForm` | Validates phone (10 digits), academic year (1–4), required fields. |

**Student portal access control:**
- A student user must have a linked `Student` record (`student.user == request.user`).
- Unlinked accounts receive HTTP 403.
- Students cannot access any admin page (HTTP 403).

---

### 3.3 `rooms` — Room Management

**Responsibility:** Hostel and room creation, listing (all, available, occupied), and room detail.

**Key components:**

| Component | Description |
|---|---|
| `models.py` — `Hostel` | Fields: `name` (unique), `block`. |
| `models.py` — `Room` | Fields: `hostel` (FK), `room_number`, `capacity` (≥ 1), `occupied_count` (0 ≤ x ≤ capacity). Unique constraint: `(hostel, room_number)`. Property: `available_beds`. |
| `views.py` — `AddHostelView` | Staff-only; creates a new hostel. |
| `views.py` — `AddRoomView` | Staff-only; creates a room under a hostel. |
| `views.py` — `RoomListView` | Staff-only; lists all rooms. |
| `views.py` — `AvailableRoomsView` | Staff-only; lists rooms with `available_beds > 0`. |
| `views.py` — `OccupiedRoomsView` | Staff-only; lists rooms with `occupied_count > 0`. |
| `views.py` — `RoomDetailView` | Staff-only; shows room details and current allocations. |
| `views.py` — `EditRoomView` | Staff-only; updates room capacity. |
| `services.py` — `RoomService` | Business logic for room validation. |

**Integrity rules (enforced by model constraints):**
- `capacity ≥ 1` (CheckConstraint)
- `0 ≤ occupied_count ≤ capacity` (CheckConstraint)
- `(hostel, room_number)` unique (UniqueConstraint)

---

### 3.4 `allocations` — Room Allocation

**Responsibility:** Allocating a room to a student, changing allocation, vacating a room, and maintaining `occupied_count` consistency.

**Key components:**

| Component | Description |
|---|---|
| `models.py` — `Allocation` | Fields: `student` (FK, PROTECT), `room` (FK, PROTECT), `active_student` (FK, nullable, unique — enforces one active allocation per student), `allocated_at`, `vacated_at`, `status` (ACTIVE / VACATED). |
| `services.py` — `AllocationService.allocate_room` | Checks capacity; creates `Allocation`; increments `room.occupied_count`. Wrapped in a database transaction. |
| `services.py` — `AllocationService.change_room` | Vacates current allocation; allocates new room. Atomic transaction. |
| `services.py` — `AllocationService.vacate_room` | Sets `status=VACATED`, `vacated_at=now()`; decrements `room.occupied_count`. Retains history. |
| `views.py` — `AllocateRoomView` | Staff-only POST; calls `AllocationService.allocate_room`. |
| `views.py` — `ChangeRoomView` | Staff-only; calls `AllocationService.change_room`. |
| `views.py` — `VacateRoomView` | Staff-only POST with confirmation; calls `AllocationService.vacate_room`. |

**Integrity rules:**
- `unique_active_allocation_per_student` (UniqueConstraint on `active_student`) — a student cannot have two active allocations simultaneously.
- `allocation_status_vacated_at_consistent` (CheckConstraint) — `ACTIVE` ↔ `vacated_at IS NULL`; `VACATED` ↔ `vacated_at IS NOT NULL`.
- `Allocation.save()` sets `active_student = student` when ACTIVE, `NULL` when VACATED.
- MySQL allows multiple NULL values in a unique column, enabling multiple vacated records per student.

---

## 4. Database Design

### 4.1 Database configuration

| Setting | Value |
|---|---|
| Engine | `django.db.backends.mysql` |
| Database name | `hostel_db` (configurable via `.env`) |
| User | `hostel_app` (configurable via `.env`) |
| Host | `127.0.0.1` (configurable via `.env`) |
| Port | `3306` (configurable via `.env`) |
| Charset | `utf8mb4` |

All credentials are read from `.env` via `python-dotenv`. No credential is committed to source code.

### 4.2 Entity–Relationship summary

```
User (Django built-in)
  │ 1
  │ N
Student ──────────── Allocation ──────────── Room
  (usn, name, email,    (student FK,           (hostel FK,
   phone, department,    room FK,               room_number,
   academic_year,        active_student FK,     capacity,
   user FK nullable)     status,                occupied_count)
                         allocated_at,
                         vacated_at)
                                                    │ N
                                                    │ 1
                                                 Hostel
                                                 (name, block)
```

### 4.3 Key constraints

| Table | Constraint | Type |
|---|---|---|
| `students_student` | `usn` unique | UNIQUE |
| `students_student` | `email` unique | UNIQUE |
| `students_student` | `academic_year` 1–4 | CHECK |
| `students_student` | `phone` 10 digits | CHECK + validator |
| `rooms_room` | `(hostel_id, room_number)` unique | UNIQUE |
| `rooms_room` | `capacity ≥ 1` | CHECK |
| `rooms_room` | `0 ≤ occupied_count ≤ capacity` | CHECK |
| `allocations_allocation` | `active_student` unique (nullable) | UNIQUE |
| `allocations_allocation` | status ↔ vacated_at consistent | CHECK |

---

## 5. Security Architecture

| Control | Implementation |
|---|---|
| Authentication | Django built-in auth; password hashed with PBKDF2 |
| Brute-force protection | `django-axes` — 5 failures / 15 min lockout per username+IP |
| Session security | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE=Lax` |
| CSRF protection | Django `CsrfViewMiddleware`; all state-changing views use POST with CSRF token |
| Clickjacking | `X_FRAME_OPTIONS=DENY` |
| Content sniffing | `SECURE_CONTENT_TYPE_NOSNIFF=True` |
| Referrer policy | `SECURE_REFERRER_POLICY=same-origin` |
| HTTPS (production) | `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS` — all configurable via `.env`; disabled for local HTTP development |
| Authorization | `is_staff` check on every admin view; HTTP 403 for non-staff |
| Input validation | Django form validators + model `CheckConstraint` + model `clean()` |
| No secrets in source | All secrets in `.env`; `.env` is git-ignored |

---

## 6. Implementation Deviations from SAD v1.0

| Area | SAD v1.0 description | Final implementation | Status |
|---|---|---|---|
| Database | SQLite for development, MySQL for production | MySQL used in both CI and local development via `.env` | Resolved |
| Student portal | Described as a future enhancement | Fully implemented in Sprint 2 (HOSTEL-33 to HOSTEL-37) | Resolved |
| Room service layer | Not described in v1.0 | `rooms/services.py` and `allocations/services.py` added for business logic separation | Addition |
| Sprint plan | v1.0 referenced a possible Sprint 3 | Project completed in exactly two sprints; no Sprint 3 | Resolved |
| `active_student` field | Not in v1.0 | Added to `Allocation` model to enforce one-active-allocation-per-student via MySQL unique constraint | Addition |
| `django-axes` | Not in v1.0 | Added for brute-force login protection (HOSTEL-38) | Addition |
| `AuthenticatedNoCacheMiddleware` | Not in v1.0 | Added to prevent back-button access after logout | Addition |

---

## 7. Open Issues

| Issue | Status |
|---|---|
| Formal usability/accessibility evaluation (HMS-NFR-001) | Not conducted; manual review only. Deferred as future work. |
| Formal load/scalability testing (HMS-NFR-006) | Out of scope for academic project. Deferred as future work. |
| Production deployment verification | Outside repository CI scope. Requires deployment-specific configuration. |

---

## 8. Future Work (Out of Scope)

- Fee and fine management
- Mess management
- Multi-hostel deployment
- Email/SMS notifications
- Report export
- Formal accessibility audit
- Load testing with representative concurrent users
