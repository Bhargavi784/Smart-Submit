✅ SmartSubmit – Backend Progress (FastAPI + PostgreSQL)

This backend powers SmartSubmit, a classroom & assignment management platform built with FastAPI, SQLAlchemy, and PostgreSQL.
Below is a clear summary of everything completed so far + instructions for your frontend teammates.

✅ Features Completed (Backend)
🔐 Authentication

User Signup (name, email, password, role)

Secure password hashing

User Login → JWT access token

Role-based access (teacher / student)

🏫 Classroom Management

Teacher creates classrooms

Auto-generated unique join codes

Students can join using join code

Fetch classroom list:

Student → Classrooms joined

Teacher → Classrooms they teach

Many-to-many relation between students ↔ classrooms

📝 Assignment System

Teachers can create assignments

Students can view assignments linked to classroom

📤 Submission System

Students submit assignment files (PDF or any file)

File stored locally in uploads/ directory

Students can view their own submissions

Teachers can view submissions inside their classroom

Teachers can grade submissions

Teachers & students can download submitted files

Secure download access (students can only download their own)

🗄 Database Models Implemented

User

Classroom

Assignment

Submission

Pivot table (student_classroom) for many-to-many

✅ How to Run Backend Locally
1) Activate Virtual Environment
venv\Scripts\activate

2) Install Dependencies
pip install -r requirements.txt

3) Start FastAPI Server
uvicorn app.main:app --reload


Server URL:

http://127.0.0.1:8000

4) API Docs (Swagger UI)
http://127.0.0.1:8000/docs

✅ Environment Requirements

Python 3.10+

PostgreSQL installed locally

Create a database & update connection string in:
app/core/database.py

Example connection URL:

postgresql://postgres:password@localhost:5432/smartsubmit

✅ Uploads Folder

All submitted files are stored inside:

uploads/


Frontend can download using:

GET /submissions/download/{submission_id}

✅ Notes for Frontend Team

JWT Token Required for all protected routes:

Authorization: Bearer <token>


File Upload Route Requires multipart/form-data

Data Flow is always:

Classroom → Assignment → Submission


Classroom list returns extra metadata:

students_count

assignments_count

✅ Backend Status

✅ Core backend fully stable
✅ Ready for complete frontend development
✅ Submission + grading + file download tested