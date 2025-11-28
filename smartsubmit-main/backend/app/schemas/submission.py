from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict, List,Union

class SubmissionBase(BaseModel):
    assignment_id: int
    classroom_id: int
    file_path: str
    remarks: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionOut(SubmissionBase):
    id: int
    student_id: int
    submitted_at: datetime
    grade: Optional[str] = None
    feedback: Optional[Dict[str, Any]] = None
    margin_report: Optional[Dict[str, Any]] = None  # JSON field

    class Config:
        from_attributes = True
