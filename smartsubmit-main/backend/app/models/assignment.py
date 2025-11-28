from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True)

    margin_top = Column(Float, nullable=True)
    margin_bottom = Column(Float, nullable=True)
    margin_left = Column(Float, nullable=True)
    margin_right = Column(Float, nullable=True)

    teacher = relationship("User")
    classroom = relationship("Classroom", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")
