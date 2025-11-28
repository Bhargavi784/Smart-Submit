from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.auth import require_role
from app.schemas.user import UserRole
from app.models.classroom import Classroom
from app.models.assignment import Assignment
from app.models.user import User
from app.core.database import get_db
from app.schemas.assignment import AssignmentCreate

router = APIRouter(prefix="/assignments")

@router.post("/create")
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.teacher))
):
    # ensure classroom belongs to current teacher
    classroom = db.query(Classroom).filter_by(
        id=assignment.classroom_id,
        teacher_id=current_user.id
    ).first()

    if not classroom:
        raise HTTPException(
            status_code=403,
            detail="You do not own this classroom."
        )

    new_assignment = Assignment(
        title=assignment.title,
        description=assignment.description,
        teacher_id=current_user.id,
        classroom_id=assignment.classroom_id,

        margin_top=assignment.margin_top or 1.0,
        margin_bottom=assignment.margin_bottom or 1.0,
        margin_left=assignment.margin_left or 1.25,
        margin_right=assignment.margin_right or 1.0
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return {
        "msg": "Assignment created successfully",
        "assignment_id": new_assignment.id,
        "classroom_id": new_assignment.classroom_id
    }


@router.get("/classroom/{classroom_id}")
def get_assignments_for_student(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.student))
):
    # check student is part of classroom
    classroom = db.query(Classroom).filter(
        Classroom.id == classroom_id,
        Classroom.students.any(id=current_user.id)
    ).first()

    if not classroom:
        raise HTTPException(status_code=403, detail="Not enrolled in this classroom")

    assignments = db.query(Assignment).filter_by(classroom_id=classroom_id).all()

    return assignments

@router.get("/teacher/{classroom_id}")
def get_assignments_for_teacher(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.teacher))
):
    classroom = db.query(Classroom).filter_by(
        id=classroom_id, teacher_id=current_user.id
    ).first()

    if not classroom:
        raise HTTPException(status_code=403, detail="Not your classroom")

    assignments = db.query(Assignment).filter_by(classroom_id=classroom_id).all()

    return assignments

