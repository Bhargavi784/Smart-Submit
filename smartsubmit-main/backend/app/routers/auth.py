from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.models.user import User, UserRole
from app.core.database import get_db
from app.utils.auth import hash_password, verify_password,create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=UserRole(user.role)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    token = create_access_token({"user_id": db_user.id, "role": db_user.role.value})
    return {"access_token": token, "token_type": "bearer"}