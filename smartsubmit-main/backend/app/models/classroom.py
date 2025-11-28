from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
import secrets

# Association table for many-to-many relationship between students and classrooms
student_classroom_table = Table(
    "student_classroom",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("classroom_id", Integer, ForeignKey("classrooms.id"), primary_key=True),
    extend_existing=True
)

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    join_code = Column(String(10), unique=True, nullable=False, default=lambda: secrets.token_hex(4))

    teacher = relationship("User", back_populates="classrooms_taught")
    students = relationship(
        "User",
        secondary=student_classroom_table,
        back_populates="classrooms_joined"
    )
    assignments = relationship("Assignment", back_populates="classroom")
    submissions = relationship("Submission", back_populates="classroom", cascade="all, delete-orphan")
