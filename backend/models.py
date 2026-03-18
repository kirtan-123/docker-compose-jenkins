from sqlalchemy import Column, DateTime, Integer, String, func, inspect, text
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    age = Column(Integer)
    department = Column(String(100))
    city = Column(String(100))
    enrollment_year = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


def ensure_student_columns() -> None:
    inspector = inspect(engine)
    if "students" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("students")}
    alter_statements = []

    if "phone" not in existing_columns:
        alter_statements.append("ALTER TABLE students ADD COLUMN phone VARCHAR(20)")
    if "age" not in existing_columns:
        alter_statements.append("ALTER TABLE students ADD COLUMN age INTEGER")
    if "department" not in existing_columns:
        alter_statements.append("ALTER TABLE students ADD COLUMN department VARCHAR(100)")
    if "city" not in existing_columns:
        alter_statements.append("ALTER TABLE students ADD COLUMN city VARCHAR(100)")
    if "enrollment_year" not in existing_columns:
        alter_statements.append("ALTER TABLE students ADD COLUMN enrollment_year INTEGER")
    if "created_at" not in existing_columns:
        alter_statements.append(
            "ALTER TABLE students ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        )

    if not alter_statements:
        return

    with engine.begin() as connection:
        for statement in alter_statements:
            connection.execute(text(statement))

Base.metadata.create_all(bind=engine)
ensure_student_columns()
