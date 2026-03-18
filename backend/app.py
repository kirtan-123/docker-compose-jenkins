from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Student

app = Flask(__name__)
Session = sessionmaker(bind=engine)


def parse_optional_int(value):
    if value in (None, ""):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def serialize_student(student):
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "phone": student.phone,
        "age": student.age,
        "department": student.department,
        "city": student.city,
        "enrollment_year": student.enrollment_year,
        "created_at": student.created_at.isoformat() if student.created_at else None,
    }


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/add", methods=["OPTIONS"])
def add_student_options():
    return "", 204

@app.route("/add", methods=["POST"])
def add_student():
    payload = request.get_json(silent=True) if request.is_json else request.form

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()

    if not name or not email:
        return jsonify({"message": "Name and email are required"}), 400

    session = Session()
    try:
        student = Student(
            name=name,
            email=email,
            phone=(payload.get("phone") or "").strip() or None,
            age=parse_optional_int(payload.get("age")),
            department=(payload.get("department") or "").strip() or None,
            city=(payload.get("city") or "").strip() or None,
            enrollment_year=parse_optional_int(payload.get("enrollment_year")),
        )
        session.add(student)
        session.commit()
        session.refresh(student)
        return jsonify({"message": "Student Added Successfully", "student": serialize_student(student)}), 201
    finally:
        session.close()


@app.route("/students", methods=["GET"])
def get_students():
    session = Session()
    try:
        students = session.query(Student).order_by(Student.id.desc()).all()
        return jsonify([serialize_student(student) for student in students])
    finally:
        session.close()

@app.route("/")
def home():
    return "Backend Running. Use /students for data."

app.run(host="0.0.0.0", port=5000)
