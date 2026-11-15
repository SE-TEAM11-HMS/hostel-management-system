# 🏠 Hostel Management System

A web-based hostel administration application built with Django and MySQL.

---

## 📌 About the Project

The Hostel Management System is a collaborative Software Engineering mini project developed at PES University. It provides a centralized web application for hostel administrators to manage student records, rooms and allocations, and for students to view their own hostel and room information through a self-service portal.

---

## 🎯 Problem Statement

Managing student records and hostel information manually is time-consuming and error-prone. This project provides a digital solution that centralizes student and room data, enforces business rules at the database level, and supports efficient hostel administration.

---

## 🎯 Objectives

- Maintain student information in a centralized system.
- Manage hostel and room records with accurate occupancy tracking.
- Allocate, change and vacate room assignments with data consistency.
- Provide students with a self-service portal to view their own room allocation.
- Apply authentication, access control and input validation throughout.
- Verify functionality through systematic automated testing.

---

## ✨ Implemented Features

### Administrator
- Login and logout with brute-force protection (5 failed attempts per username/IP triggers a 15-minute lockout)
- Student record management: add, view, update, delete and search
- Hostel and room management: create hostels and rooms, view all rooms, available rooms and occupied rooms
- Room allocation: allocate a room to a student, change allocation, vacate a room
- View a student's current and historical room allocation

### Student Portal
- Student login (separate login page at `/student-login/`)
- View own profile: USN, name, email, phone, department and academic year
- View own active room and hostel allocation

---

## 🧩 System Modules

| Module | Responsibility |
|---|---|
| `accounts` | Login, logout, administrator dashboard, session management, no-cache middleware |
| `students` | Student CRUD, search, student portal, student–user account association |
| `rooms` | Hostel and room creation, room listing (all, available, occupied), room detail |
| `allocations` | Room allocation, room change, room vacation, occupancy consistency |

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.11 or newer |
| Web framework | Django | 5.2.18 |
| Database | MySQL | 8.0 |
| Database driver | mysqlclient | 2.3.0 |
| Brute-force protection | django-axes | 9.0.0 |
| Environment configuration | python-dotenv | 1.2.4 |
| Version control | Git | — |
| CI platform | GitHub Actions | — |

---

## 💻 Prerequisites

Install the following before setting up the project:

1. **Python 3.11 or newer** — https://www.python.org/downloads/
2. **MySQL 8.0** — https://dev.mysql.com/downloads/mysql/
3. **MySQL development headers** (required to build `mysqlclient`):
   - **Windows:** Install the full MySQL installer which includes the C connector and development headers.
   - **Ubuntu/Debian:** `sudo apt-get install pkg-config default-libmysqlclient-dev build-essential`
   - **macOS:** `brew install mysql-client pkg-config`
4. **Git** — https://git-scm.com/

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SE-TEAM11-HMS/hostel-management-system.git
cd hostel-management-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows — Command Prompt:**
```cmd
venv\Scripts\activate
```

**Windows — Git Bash:**
```bash
source venv/Scripts/activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

> If `mysqlclient` fails to build, ensure the MySQL development headers are installed (see Prerequisites above).

### 4. Configure MySQL

#### 4a. Create the database and application user

Log in to MySQL as root and run the following commands. Replace `<your-password>` with a strong password of your choice:

```sql
CREATE DATABASE hostel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hostel_app'@'127.0.0.1' IDENTIFIED BY '<your-password>';
GRANT ALL PRIVILEGES ON hostel_db.* TO 'hostel_app'@'127.0.0.1';
GRANT CREATE, DROP ON *.* TO 'hostel_app'@'127.0.0.1';
FLUSH PRIVILEGES;
```

The Django test runner creates and drops a separate database named `test_hostel_db`. MySQL requires global `CREATE` and `DROP` privileges for those operations, so grant them only to this local development account. Do not reuse this account in production; production should use separate credentials limited to its application database.

#### 4b. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and update the following values:

```
SECRET_KEY=<generate-a-random-secret-key>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=hostel_db
DB_USER=hostel_app
DB_PASSWORD=<your-password>
DB_HOST=127.0.0.1
DB_PORT=3306
```

To generate a `SECRET_KEY`, run:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

> **Important:** Never commit `.env` to version control. It is already listed in `.gitignore`. Do not share or expose your `SECRET_KEY` or database password.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username and password. This account will have `is_staff=True` and can log in at `/login/`.

### 7. Start the development server

```bash
python manage.py runserver
```

Open your browser at: http://127.0.0.1:8000/login/

---

## 🔑 Login

| Role | Login URL | Credentials |
|---|---|---|
| Administrator | `/login/` | Username and password set via `createsuperuser` |
| Student | `/student-login/` | Username and password of a linked student user account |

To create a student user account, log in as administrator, create a student record, then link a Django user account to that student via the Django admin panel at `/admin/`.

---

## 🧪 Running Tests

Run the complete automated test suite:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test accounts
python manage.py test students
python manage.py test rooms
python manage.py test allocations
```

Run only the regression tests:

```bash
python manage.py test students.test_regression
```

Run only the security tests:

```bash
python manage.py test students.test_security
```

The test suite uses Django's test runner which creates a temporary MySQL test database and destroys it after the run. No data in `hostel_db` is affected.

---

## ⚙️ GitHub Actions CI

The CI workflow (`.github/workflows/ci.yml`) runs automatically on every push and pull request:

1. Starts a MySQL 8.0 service container.
2. Installs Python 3.14 and MySQL system dependencies.
3. Installs Python dependencies from `requirements.txt`.
4. Runs `python manage.py check`.
5. Applies migrations with `python manage.py migrate`.
6. Runs the full test suite with `python manage.py test`.

All CI credentials are set as environment variables in the workflow file. No real password or secret is stored in the repository.

---

## 📁 Project Structure

```
hostel-management-system/
├── accounts/               # Login, logout, dashboard, middleware
│   ├── views.py
│   ├── forms.py
│   ├── middleware.py
│   └── tests.py
├── students/               # Student CRUD, search, student portal
│   ├── views.py
│   ├── forms.py
│   ├── models.py
│   ├── portal_urls.py
│   ├── tests.py
│   ├── test_integration.py
│   ├── test_security.py
│   ├── test_regression.py
│   └── test_nonfunctional.py
├── rooms/                  # Hostel and room management
│   ├── views.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   └── tests.py
├── allocations/            # Room allocation, change, vacation
│   ├── views.py
│   ├── models.py
│   ├── services.py
│   └── tests.py
├── hostel_project/         # Django settings and URL configuration
│   ├── settings.py
│   └── urls.py
├── docs/                   # SRS, STP, SAD, RTM, test reports
├── .env.example            # Environment variable template
├── .github/workflows/      # GitHub Actions CI workflow
├── manage.py
└── requirements.txt
```

---

## 🔐 Security Notes

- All secrets (`SECRET_KEY`, database password) must be set in `.env` and never committed to the repository.
- `.env` is listed in `.gitignore`.
- Login brute-force protection is enabled by default: 5 failed attempts per username/IP triggers a 15-minute lockout. Adjust `AXES_FAILURE_LIMIT` and `AXES_COOLOFF_MINUTES` in `.env` if required.
- For production deployment, set `DEBUG=False`, configure `ALLOWED_HOSTS`, and enable `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` and `SECURE_HSTS_SECONDS` in `.env`.

---

## 📄 Project Documentation

| Document | Location |
|---|---|
| Software Requirements Specification (SRS) | [Open PDF](docs/SRS_Hostel_management_system_team11.pdf) |
| Software Test Plan (STP) | [Open PDF](docs/STP_Hostel_Management_system_team11.pdf) |
| Software Architecture and Design (SAD v2.0) | [View document](docs/HOSTEL-47-sad-v2.md) |
| Requirements Traceability Matrix — Sprint 1 | [View document](docs/RTM_Sprint1.md) |
| Requirements Traceability Matrix — Sprint 2 Final | [View document](docs/HOSTEL-45-rtm-sprint2-final.md) |
| Final Test Summary Report | [View document](docs/HOSTEL-46-final-test-summary-report.md) |
| Sprint 2 Acceptance RTM | [View document](docs/RTM_Sprint2_Acceptance.md) |
| Sprint 1 Demo Video | [Watch video](docs/sprint1_demo.mp4) |

---

## 👥 Team Members

| Name | Role |
|---|---|
| Pavithra G C | Implementation, testing, documentation |
| Pavan Kumar H S | Implementation, testing, documentation |
| Prabhakar Kumar | Implementation, testing, documentation |
| Pradeep | Implementation, testing, documentation |

---

## 🎓 Academic Information

| Detail | Information |
|---|---|
| Project | Hostel Management System |
| Department | Computer Science and Engineering |
| Institution | PES University |
| Project type | Software Engineering Mini Project |
| Team | Team 11 |
| Sprints | 2 (Sprint 1: authentication and student management; Sprint 2: rooms, allocation, portal, testing and documentation) |

---

*Developed as part of the Software Engineering mini project at PES University.*
