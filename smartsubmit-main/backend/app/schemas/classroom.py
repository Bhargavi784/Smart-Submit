from pydantic import BaseModel
from typing import Optional

class ClassroomCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ClassroomJoin(BaseModel):
    join_code: str

class ClassroomOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    teacher_id: Optional[int] = None
    join_code: str
    students_count: int
    assignments_count: int

    class Config:
        from_attributes = True
