# 🏠 Hostel Management System

A web-based application for managing hostel student records and hostel-related information.

## 📌 About the Project

The Hostel Management System is a collaborative Software Engineering mini project developed to simplify hostel administration through a centralized web application.

The project focuses on organizing student information, supporting hostel administration, and improving the management of student records.

## 🎯 Problem Statement

Managing student records and hostel information manually can be time-consuming and prone to errors. Maintaining accurate, up-to-date information can also become difficult as the number of students increases.

This project aims to provide a digital solution that improves data organization, reduces repetitive manual work, and supports efficient hostel administration.

## 🎯 Objectives

- Maintain student information in a centralized system.
- Simplify student record management.
- Improve the organization of hostel-related information.
- Apply authentication and access control where required.
- Validate functionality through systematic testing.
- Develop a maintainable web application using Python and Django.

## ✨ Key Features

The project focuses on the following functional areas:

- Student record management.
- Student information retrieval.
- Student detail updates, where supported.
- Authentication and access control.
- Validation of user requests.
- Security testing for unauthorized actions.

Additional features will be documented as they are implemented.

## 🧩 System Modules

### 1. Authentication and Access Control

- Handle authenticated access.
- Enforce permissions for protected operations.
- Prevent unauthorized actions.

### 2. Student Management

- Manage student records.
- Retrieve student information.
- Support student detail updates where implemented.

### 3. Data Management

- Store and retrieve application data.
- Maintain consistency of student records.

### 4. Testing and Validation

- Verify application functionality.
- Test access permissions.
- Check expected responses for unauthorized requests.

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Web Framework:** Django
- **Testing:** Django Test Framework
- **Version Control:** Git
- **Repository Hosting:** GitHub
- **Development Environment:** Visual Studio Code
- **Database:** The database configured in the project's Django settings.

## 💻 Prerequisites

Before running the project, ensure that you have installed:

- Python 3
- Git
- pip
- A terminal or command-line interface

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SE-TEAM11-HMS/hostel-management-system.git
cd hostel-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it in Windows Git Bash:

```bash
source venv/Scripts/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

Open the following address in your browser:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

> Run these commands from the project root directory. The available features depend on the current implementation.

## 🧪 Testing

The project uses Django's testing framework to verify application behavior.

Run the complete test suite:

```bash
python manage.py test
```

Testing includes relevant areas such as:

- Student management functionality.
- Authentication and permissions.
- Unauthorized access prevention.
- Request validation.
- Expected HTTP responses.
- Data integrity after restricted operations.

## 🔐 Security

Security-related testing helps verify that protected operations are accessible only to authorized users.

Security considerations include:

- Authentication requirements.
- Permission checks.
- Protection against unauthorized student record deletion.
- Request validation.
- Verification that restricted operations do not modify protected data.

## 📁 Project Structure

The repository contains the Django application, its configuration, student management code, and associated tests.

Explore the project repository:

[View the Hostel Management System on GitHub](https://github.com/SE-TEAM11-HMS/hostel-management-system)

## 👥 Team Members

| Team Member |
|---|
| Pavithra G C |
| Pavan Kumar H S |
| Prabhakar Kumar |
| Pradeep |

## 📄 Project Documentation

The project documentation covers requirements analysis and Software Engineering deliverables, including:

- Software Requirements Specification (SRS).
- Functional and non-functional requirements.
- UML use-case diagrams.
- Acceptance test cases.
- Requirements Traceability Matrix (RTM).

Refer to the repository for the available documentation files.

## 📊 Project Status

The project is being developed collaboratively as part of Software Engineering coursework.

Development, testing, and documentation progress may change as features are implemented and verified.

## 🎓 Academic Information

| Detail | Information |
|---|---|
| Project | Hostel Management System |
| Department | Computer Science and Engineering |
| Institution | PES University |
| Project Type | Software Engineering Mini Project |
| Team Size | 4 |

## 🤝 Contribution

This is a collaborative academic project. Team members contribute to implementation, documentation, testing, and project improvement.

Changes should be developed and reviewed in coordination with the team to maintain code quality and avoid conflicts.

## 📌 Expected Outcome

The expected outcome is a maintainable web application that supports organized student record management and improves the efficiency of hostel administration.

The project also provides practical experience with web development, access control, software testing, version control, and collaborative development.

---

*Developed as part of the Software Engineering mini project at PES University.*