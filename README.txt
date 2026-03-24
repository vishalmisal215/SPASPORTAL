══════════════════════════════════════════════════════
  SPAS — Student Practical Assessment System
  With Attendance Module
══════════════════════════════════════════════════════

HOW TO RUN
──────────
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   python app.py

3. Open browser:
   http://localhost:5000

DEFAULT LOGINS
──────────────
Student login  → use any roll_no from data/users.json
                 e.g.  Roll: 24051012  Password: CSS24051012

Faculty login  → Faculty ID: FAC001   Password: faculty123

PROJECT STRUCTURE
─────────────────
  app.py                    ← Main Flask application
  requirements.txt          ← pip packages
  data/
    users.json              ← Student accounts
    faculty.json            ← Faculty accounts
    subjects.json           ← Subjects + practicals
    practicals.json         ← Dynamic practicals list
    questions.json          ← Exam questions
    attendance.json         ← Attendance sessions (auto-created)
    results/                ← Exam result files
  static/
    css/style.css
    js/script.js            ← Student JS
    js/faculty_script.js    ← Faculty JS
  templates/
    base.html               ← Student base layout
    login.html
    dashboard.html          ← Student dashboard (+ attendance)
    exam.html
    result.html
    faculty_dashboard.html  ← Faculty dashboard (+ attendance)

ATTENDANCE FEATURES
───────────────────
FACULTY:
  • Click "Attendance" in nav
  • Select Subject + Batch
  • Set validity minutes → Generate Code
  • Code shows as large 6-char display with countdown bar
  • Calendar date picker → View Attendance (filterable by Subject/Batch/Date)
  • Download Excel → colour-coded P/A sheet per student

STUDENT:
  • Click "Attendance" in nav
  • Enter 6-char code → Mark Present
  • My Attendance Summary shows % per subject
    🟢 ≥75%  🟠 <65%  🔴 <60%
  • Warning banner auto-shown if below 75%
══════════════════════════════════════════════════════
