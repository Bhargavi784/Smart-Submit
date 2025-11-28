from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form,status
from sqlalchemy.orm import Session
from datetime import datetime
import os
import mimetypes
from fastapi.responses import FileResponse
from app.core.database import get_db
from app.models.submission import Submission
from app.models.assignment import Assignment
from app.models.classroom import Classroom
from app.models.user import UserRole, User
from app.utils.auth import get_current_user, require_role
from app.utils.grammar_checker import check_pdf_grammar
from app.utils.pdf_margin_checker import check_pdf_margins
from app.schemas.submission import SubmissionCreate, SubmissionOut

router = APIRouter(prefix="/submissions", tags=["Submissions"])

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# STUDENT: Submit assignment

@router.post("/submit", response_model=SubmissionOut)
async def submit_assignment(
    assignment_id: int = Form(...),
    classroom_id: int = Form(...),
    file: UploadFile = File(...),
    remarks: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student))
):
    """
    Student submits an assignment PDF.
    Automatically performs a margin check and stores the results.
    """

    # ✅ 1. Validate classroom & assignment
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not classroom or not assignment:
        raise HTTPException(status_code=404, detail="Classroom or assignment not found")

    if assignment.classroom_id != classroom.id:
        raise HTTPException(status_code=400, detail="Assignment does not belong to this classroom")

    # ✅ 2. Save uploaded file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # ✅ 3. Run margin check (using improved checker)
    required_margins = {
        "top":assignment.margin_top or 1.0,
        "left":assignment.margin_left or 1.25,
        "right":assignment.margin_right or 1.0
    }

    try:
        margin_result = check_pdf_margins(file_path, required_margins)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Margin check failed: {str(e)}")
    
    grammar_result = check_pdf_grammar(file_path)


    # ✅ 4. Create submission entry
    submission = Submission(
        student_id=current_user.id,
        classroom_id=classroom.id,
        assignment_id=assignment.id,
        file_path=file_path,
        submitted_at=datetime.utcnow(),
        remarks=remarks,
        margin_report=margin_result,
        feedback=grammar_result
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    if isinstance(submission.feedback, str):
        import json
        submission.feedback = json.loads(submission.feedback)
    # ✅ 5. Return saved submission
    return submission


# TEACHER: View all submissions in their classroom

@router.get("/classroom/{classroom_id}", response_model=list[SubmissionOut])
def get_classroom_submissions(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.teacher))
):
    classroom = db.query(Classroom).filter_by(id=classroom_id, teacher_id=current_user.id).first()
    if not classroom:
        raise HTTPException(status_code=403, detail="You are not the teacher of this classroom")

    submissions = db.query(Submission).filter(Submission.classroom_id == classroom_id).all()
    return submissions

# STUDENT: View their own submissions

@router.get("/my", response_model=list[SubmissionOut])
def get_my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student))
):
    submissions = db.query(Submission).filter(Submission.student_id == current_user.id).all()
    return submissions

@router.post("/grade/{submission_id}")
def grade_submission(
    submission_id: int,
    grade: int = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.teacher))
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission.grade = grade
    submission.teacher_feedback = feedback  # NEW FIELD
    db.commit()
    return {"msg": "Grade submitted!"}


@router.get("/download/{submission_id}")
def download_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")

    # Security check: only owner student or the classroom's teacher
    if current_user.role == UserRole.student:
        if submission.student_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    elif current_user.role == UserRole.teacher:
        classroom = db.query(Classroom).filter(Classroom.id == submission.classroom_id).first()
        if not classroom or classroom.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        raise HTTPException(status_code=403, detail="Access denied")

    file_path = submission.file_path  # <-- important: file_path (not file_url)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    mime, _ = mimetypes.guess_type(file_path)
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type=mime or "application/octet-stream",
    )
@router.get("/student/{assignment_id}", response_model=SubmissionOut)
def get_student_submission(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student))
):
    submission = db.query(Submission).filter(
        Submission.assignment_id == assignment_id,
        Submission.student_id == current_user.id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission
