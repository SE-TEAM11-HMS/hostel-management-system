# 🏠 Hostel Management System

A web-based application for managing hostel student records, room allocations, and hostel administration.

---

## 📌 About the Project

The Hostel Management System is a collaborative Software Engineering mini project developed at PES University. It provides a centralized Django web application for hostel administrators to manage student records, rooms, and allocations, and for students to view their own hostel and room information through a self-service portal.

---

## ✨ Implemented Features

### Administrator
- Login and logout with brute-force protection (5 attempts / 15-minute lockout)
- Student record management: add, view, update, delete, and search
- Hostel and room management: create hostels and rooms, view available and occupied rooms
- Room allocation: allocate a room to a student, change allocation, vacate a room
- View a student's current and historical room allocation

### Student Portal
- Student login (separate login page)
- View own profile (USN, name, email, phone, department, academic year)
- View own active room and hostel allocation

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 or newer |
| Web framework | Django 5.2 |
| Database | MySQL 8.0 |
| Database driver | mysqlclient 2.3.0 |
| Brute-force protection | django-axes 9.0.0 |
| Environment config | python-dotenv 1.2.4 |
| CI | GitHub Actions (Ubuntu, Python 3.14, MySQL 8.0) |

---

## 💻 Prerequisites

Before running the project, install:

1. **Python 3.11 or newer** — <https://www.python.org/downloads/>
2. **MySQL 8.0** — <https://dev.mysql.com/downloads/mysql/>
3. **MySQL system libraries** (required to build `mysqlclient`):
   - **Windows:** Install [MySQL Connector/C](https://dev.mysql.com/downloads/connector/c/) or the full MySQL installer which includes the development headers.
   - **Ubuntu/Debian:** `sudo apt-get install pkg-config default-libmysqlclient-dev build-essential`
   - **macOS:** `brew install mysql-client pkg-config`
4. **Git** — <https://git-scm.com/>
5. **pip** (included with Python)

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

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (Git Bash):**
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

Log in to MySQL as root and run:

```sql
CREATE DATABASE hostel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hostel_app'@'127.0.0.1' IDENTIFIED BY '<your-password>';
GRANT ALL PRIVILEGES ON hostel_db.* TO 'hostel_app'@'127.0.0.1';
FLUSH PRIVILEGES;
```

Replace `<your-password>` with a strong password of your choice.

#### 4b. Configure environment variables

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

Open `.env` and set the following values:

```
SECRET_KEY=<generate-a-random-50-character-string>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=hostel_db
DB_USER=hostel_app
DB_PASSWORD=<your-password>
DB_HOST=127.0.0.1
DB_PORT=3306
```

**Important:** Never commit `.env` to version control. It is already listed in `.gitignore`.

To generate a `SECRET_KEY`, run:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

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

Open your browser at: <http://127.0.0.1:8000/login/>

---

## 🔑 Login

| Role | URL | Credentials |
|---|---|---|
| Administrator | `/login/` | Username and password set via `createsuperuser` |
| Student | `/student-login/` | Username and password of a student user account |

To create a student user account, log in as administrator, create a student record, and then link a Django user account to that student via the Django admin panel at `/admin/`.

---

## 🧪 Testing

Run the complete automated test suite:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test students
python manage.py test rooms
python manage.py test allocations
python manage.py test accounts
```

Run only the regression tests:

```bash
python manage.py test students.test_regression
```

The test suite uses Django's test database (a temporary MySQL database created and destroyed automatically). No data in `hostel_db` is affected.

---

## ⚙️ CI Workflow

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

1. Starts a MySQL 8.0 service container.
2. Installs Python 3.14 and MySQL system dependencies.
3. Installs Python dependencies from `requirements.txt`.
4. Runs `python manage.py check`.
5. Applies migrations.
6. Runs `python manage.py test`.

All credentials used in CI are environment variables set in the workflow file. No real password or secret is stored in the repository.

---

## 📁 Project Structure

```
hostel-management-system/
├── accounts/          # Login, logout, dashboard, middleware
├── allocations/       # Room allocation, change, vacation
├── rooms/             # Hostel and room management
├── students/          # Student CRUD, search, portal
├── hostel_project/    # Django settings, URL configuration
├── docs/              # SRS, STP, SAD, RTM, test reports, demo video
├── .env.example       # Environment variable template
├── manage.py
└── requirements.txt
```

---

## 📄 Project Documentation

| Document | Location |
|---|---|
| Software Requirements Specification (SRS) | `docs/SRS_Hostel_management_system_team11.pdf` |
| Software Test Plan (STP) | `docs/STP_Hostel_Management_system_team11.pdf` |
| Software Architecture and Design (SAD v2.0) | `docs/HOSTEL-47-sad-v2.md` |
| Requirements Traceability Matrix — Sprint 1 | `docs/RTM_Sprint1.md` |
| Requirements Traceability Matrix — Sprint 2 Final | `docs/HOSTEL-45-rtm-sprint2-final.md` |
| Sprint 2 Acceptance RTM | `docs/RTM_Sprint2_Acceptance.md` |
| Final Test Summary Report | `docs/HOSTEL-46-final-test-summary-report.md` |
| Sprint 2 Test Summary Report | `docs/Sprint2_Test_Summary_Report.md` |
| Sprint 1 Demo Video | `docs/sprint1_demo.mp4` |

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
| Sprints | 2 (Sprint 1: authentication + student management; Sprint 2: rooms + allocation + portal + testing) |

---

## 🔐 Security Notes

- All secrets (`SECRET_KEY`, database password) must be set in `.env` and never committed to the repository.
- The `.env` file is listed in `.gitignore`.
- For production deployment, set `DEBUG=False`, configure `ALLOWED_HOSTS`, enable `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, and set `SECURE_HSTS_SECONDS` appropriately.

---

*Developed as part of the Software Engineering mini project at PES University.*
