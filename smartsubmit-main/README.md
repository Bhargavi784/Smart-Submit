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

# 🎨 **Frontend – SmartSubmit (HTML + TailwindCSS + JavaScript)**

The frontend of SmartSubmit is built using **HTML**, **Tailwind CSS**, and **JavaScript**, and is served directly through FastAPI using `StaticFiles`.
All pages, scripts, and assets live inside:

```
backend/app/static/
```

This keeps the entire project (frontend + backend + file handling) running on a single server for easy development and deployment.

---

## 📁 **Frontend Folder Structure**

```
backend/
└── app/
    ├── routers/
    ├── schemas/
    ├── static/
    │   ├── js/
    │   │   ├── auth.js
    │   │   ├── classroom.js
    │   │   ├── create_assignment.js
    │   │   ├── dashboard.js
    │   │   ├── submission.js
    │   │   ├── teacher_submissions.js
    │   │   └── utils.js
    │   ├── index.html
    │   ├── dashboard.html
    │   ├── classroom.html
    │   ├── create_assignment.html
    │   ├── submission.html
    │   └── teacher_submissions.html
    ├── main.py
    └── uploads/
```

---

## ✅ **Frontend Features**

### 🔐 Authentication

* Login using email & password
* JWT token saved in `localStorage`
* Users redirected based on role (teacher / student)
* Token auto-attached to every protected API call

### 🏫 Classroom Pages

* Students: Join classroom using join code
* Teachers: Create classrooms
* Both roles: View classroom list with

  * `students_count`
  * `assignments_count`

### 📝 Assignments

* Teacher: Create assignments
* Student: View assignments linked to classroom
* Dynamic rendering using JavaScript fetch calls

### 📤 Submissions

* Students upload files (`multipart/form-data`)
* Students view previous submissions
* Teachers view all submissions per classroom
* Teachers grade submissions
* Secure file download buttons for teacher & student

---

## 📡 **API Integration (Frontend → Backend)**

### Authorization Header

```
Authorization: Bearer <token>
```

### Example GET Request

```js
fetch(`${BASE_URL}/classrooms`, {
  headers: {
    "Authorization": "Bearer " + localStorage.getItem("token")
  }
});
```

### Example File Upload Request

```js
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch(`${BASE_URL}/submissions/upload/${assignmentId}`, {
  method: "POST",
  headers: {
    "Authorization": "Bearer " + localStorage.getItem("token")
  },
  body: formData
});
```

---

## ▶️ **How to Run the Frontend**

The frontend needs **no separate server**.

Start the FastAPI backend:

```
uvicorn app.main:app --reload
```

Then open:

```
http://127.0.0.1:8000/static/index.html
```

All HTML pages load directly from the static directory:

* `/static/index.html`
* `/static/dashboard.html`
* `/static/create_assignment.html`
* `/static/classroom.html`
* `/static/submission.html`
* `/static/teacher_submissions.html`

---

## 🌐 **Base API URL Configuration**

Inside `utils.js` (or at the top of each JS file):

```js
const BASE_URL = "http://127.0.0.1:8000";
```

---

## 🧭 **Frontend Flow**

```
Login → Dashboard → Classroom → Assignment → Submission
```

Matches backend structure:

```
Classroom → Assignment → Submission
```

---

## 🟢 **Frontend Status**

✔ Fully functional
✔ Integrated with backend
✔ All main workflows complete
✔ Ready for deployment
