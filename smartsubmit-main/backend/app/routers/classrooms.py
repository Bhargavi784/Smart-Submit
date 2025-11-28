from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session,joinedload
from typing import List
from app.schemas.classroom import ClassroomCreate,ClassroomJoin, ClassroomOut
from app.schemas.user import UserRole
from app.models.classroom import Classroom,student_classroom_table
from app.models.user import UserRole,User
from app.utils.auth import require_role,get_current_user
from app.core.database import get_db

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])

# Teacher creates a classroom
@router.post("/create")
def create_classroom(
    classroom: ClassroomCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.teacher))
):
    new_classroom = Classroom(
        name=classroom.name,
        description=classroom.description,
        teacher_id=current_user.id
    )
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return {
        "msg": f"Classroom '{new_classroom.name}' created",
        "classroom_id": new_classroom.id,
        "join_code": new_classroom.join_code
    }

# Student joins a classroom
@router.post("/join", response_model=ClassroomOut)
def join_classroom(
    data: ClassroomJoin,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student))
):
    classroom = db.query(Classroom).filter_by(join_code=data.join_code).first()
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")

    current_user = db.merge(current_user)

    # Check if already joined
    if current_user in classroom.students:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already joined this classroom")

    classroom.students.append(current_user)
    db.commit()
    db.refresh(classroom)

    # compute counts manually
    students_count = len(classroom.students)
    assignments_count = len(classroom.assignments)

    # return data matching ClassroomOut schema
    return {
        "id": classroom.id,
        "name": classroom.name,
        "description": classroom.description,
        "teacher_id": classroom.teacher_id,
        "join_code": classroom.join_code,
        "students_count": students_count,
        "assignments_count": assignments_count
    }


# Get classrooms joined by a student OR taught by a teacher
@router.get("/joined", response_model=List[ClassroomOut])
def get_joined_classrooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user = db.query(User).options(
        joinedload(User.classrooms_joined).joinedload(Classroom.students),
        joinedload(User.classrooms_joined).joinedload(Classroom.assignments),
        joinedload(User.classrooms_taught).joinedload(Classroom.students),
        joinedload(User.classrooms_taught).joinedload(Classroom.assignments)
    ).filter(User.id == current_user.id).first()

    classrooms_list = []

    if current_user.role.name == "student":
        classrooms = current_user.classrooms_joined
    elif current_user.role.name == "teacher":
        classrooms = current_user.classrooms_taught
    else:
        raise HTTPException(status_code=403, detail="Forbidden: Unknown role")

    for c in classrooms:
        classrooms_list.append(
            ClassroomOut(
                id=c.id,
                name=c.name,
                description=c.description,
                join_code=c.join_code,
                students_count=len(c.students),
                assignments_count=len(c.assignments)                
            )
        )

    return classrooms_list