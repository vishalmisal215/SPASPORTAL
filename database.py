"""
SPAS — Database Models (SQLite via Flask-SQLAlchemy)
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """Student accounts"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    plain_password = db.Column(db.String(256), default="")
    full_name = db.Column(db.String(120), nullable=False, default="")
    branch = db.Column(db.String(50), default="")
    year = db.Column(db.String(10), default="")
    batch = db.Column(db.String(10), default="1")
    email = db.Column(db.String(120), default="")

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
        self.plain_password = pw

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "full_name": self.full_name,
            "branch": self.branch,
            "year": self.year,
            "batch": self.batch,
            "email": self.email,
        }


class Faculty(db.Model):
    """Faculty accounts"""
    __tablename__ = "faculty"
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    plain_password = db.Column(db.String(256), default="")
    full_name = db.Column(db.String(120), nullable=False, default="")
    department = db.Column(db.String(100), default="")
    email = db.Column(db.String(120), default="")
    subjects = db.Column(db.String(500), default="")

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
        self.plain_password = pw

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def to_dict(self):
        return {
            "faculty_id": self.faculty_id,
            "full_name": self.full_name,
            "department": self.department,
            "email": self.email,
            "subjects": self.subjects,
        }


class Subject(db.Model):
    """Subjects (e.g. CSS, IFS)"""
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.String(10), default="")
    practicals = db.relationship("Practical", backref="subject", lazy=True,
                                 order_by="Practical.sort_order")

    def to_dict(self, include_practicals=True):
        d = {"id": str(self.id), "name": self.name, "year": self.year}
        if include_practicals:
            d["practicals"] = [p.name for p in self.practicals]
        return d


class Practical(db.Model):
    """Practicals linked to a subject"""
    __tablename__ = "practicals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    sort_order = db.Column(db.Integer, default=9999)

    questions = db.relationship("Question", backref="practical", lazy=True)


class Question(db.Model):
    """MCQ questions linked to a practical"""
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    practical_id = db.Column(db.Integer, db.ForeignKey("practicals.id"), nullable=False)
    practical_name = db.Column(db.String(500), default="")  # denormalized for fast lookup
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), default="")
    option_b = db.Column(db.String(500), default="")
    option_c = db.Column(db.String(500), default="")
    option_d = db.Column(db.String(500), default="")
    answer = db.Column(db.String(1), nullable=False)  # A/B/C/D

    def to_dict(self):
        return {
            "id": self.id,
            "practical": self.practical_name,
            "question": self.question,
            "options": {
                "A": self.option_a,
                "B": self.option_b,
                "C": self.option_c,
                "D": self.option_d,
            },
            "answer": self.answer,
        }


class Result(db.Model):
    """Exam results (replaces .txt files)"""
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), nullable=False, index=True)
    name = db.Column(db.String(120), default="")
    branch = db.Column(db.String(50), default="")
    year = db.Column(db.String(10), default="")
    batch = db.Column(db.String(10), default="1")
    email = db.Column(db.String(120), default="")
    practical_name = db.Column(db.String(500), nullable=False)
    score = db.Column(db.String(20), default="0 / 0")
    attempted = db.Column(db.Integer, default=0)
    correct = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    datetime_str = db.Column(db.String(30), default="")
    timestamp = db.Column(db.Integer, default=0)  # Unix timestamp for dedup
    details_json = db.Column(db.Text, default="[]")  # JSON string of detailed answers

    def to_dict(self):
        import json
        return {
            "Roll No": self.roll_no,
            "Name": self.name,
            "Branch": self.branch,
            "Year": self.year,
            "Batch": self.batch,
            "Email": self.email,
            "Practical": self.practical_name,
            "Score": self.score,
            "Attempted": str(self.attempted),
            "Correct": str(self.correct),
            "Wrong": str(self.wrong),
            "Date & Time": self.datetime_str,
        }

    def to_full_dict(self):
        import json
        d = {
            "roll_no": self.roll_no,
            "name": self.name,
            "branch": self.branch,
            "year": self.year,
            "batch": self.batch,
            "email": self.email,
            "practical_name": self.practical_name,
            "score": self.score,
            "attempted": self.attempted,
            "correct": self.correct,
            "wrong": self.wrong,
            "datetime": self.datetime_str,
            "detailed_answers": json.loads(self.details_json) if self.details_json else [],
        }
        return d

    def to_txt(self):
        """Generate the same .txt format as the old system for downloads"""
        import json
        lines = [
            f"Roll No: {self.roll_no}",
            f"Name: {self.name}",
            f"Branch: {self.branch}",
            f"Year: {self.year}",
            f"Batch: {self.batch}",
            f"Email: {self.email}",
            f"Practical: {self.practical_name}",
            f"Score: {self.score}",
            f"Attempted: {self.attempted}",
            f"Correct: {self.correct}",
            f"Wrong: {self.wrong}",
            f"Date & Time: {self.datetime_str}",
            "",
            "========== QUESTION WISE RESULT =========="
        ]
        detailed = json.loads(self.details_json) if self.details_json else []
        for i, item in enumerate(detailed, 1):
            lines.append("")
            lines.append(f"Q{i}. {item.get('question', '')}")
            opts = item.get("options", {})
            for key in ["A", "B", "C", "D"]:
                lines.append(f"   {key}) {opts.get(key, '')}")
            lines.append(f"Your Answer   : {item.get('student_answer', '')}")
            lines.append(f"Correct Answer: {item.get('correct_answer', '')}")
            lines.append(f"Status        : {item.get('status', '')}")
            lines.append("-" * 50)
        return "\n".join(lines)


class AttendanceSession(db.Model):
    """Attendance sessions created by faculty"""
    __tablename__ = "attendance_sessions"
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    code = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(100), default="")
    batch = db.Column(db.String(10), default="all")
    date = db.Column(db.String(20), default="")
    created_at = db.Column(db.Integer, default=0)
    valid_seconds = db.Column(db.Integer, default=600)

    records = db.relationship("AttendanceRecord", backref="session", lazy=True)


class AttendanceRecord(db.Model):
    """Individual attendance marks"""
    __tablename__ = "attendance_records"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("attendance_sessions.id"), nullable=False)
    roll_no = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120), default="")
    marked_at = db.Column(db.Integer, default=0)
