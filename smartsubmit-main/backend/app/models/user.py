from sqlalchemy import Column, Integer, String, Enum, ForeignKey,Table
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class UserRole(enum.Enum):
    student = "student"
    teacher = "teacher"

student_classroom_table = Table(
    "student_classroom",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("classroom_id", Integer, ForeignKey("classrooms.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    classrooms_taught = relationship("Classroom", back_populates="teacher")
    classrooms_joined = relationship(
        "Classroom",
        secondary=student_classroom_table,
        back_populates="students"
    )
    submissions = relationship("Submission", back_populates="student", cascade="all, delete-orphan")
