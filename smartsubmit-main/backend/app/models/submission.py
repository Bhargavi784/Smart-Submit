from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"))
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"))

    file_path = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    feedback = Column(JSON, nullable=True)
    grade = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)
    margin_report = Column(JSON, nullable=True)

    # Relationships
    student = relationship("User", back_populates="submissions")
    classroom = relationship("Classroom", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    teacher_feedback = Column(String, nullable=True)

