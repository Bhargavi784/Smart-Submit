from pydantic import BaseModel
from typing import Optional

class AssignmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    classroom_id: int

    margin_top: Optional[float] = None
    margin_bottom: Optional[float] = None
    margin_left: Optional[float] = None
    margin_right: Optional[float] = None