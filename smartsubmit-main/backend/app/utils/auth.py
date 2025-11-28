from fastapi import Depends, HTTPException, status
from app.schemas.user import UserRole
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.models.user import User
from app.core.database import SessionLocal
from app.schemas.user import UserRole
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    print(f"Password received for hashing: {password!r}, length: {len(password)}")
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: UserRole):
    async def wrapper(current_user: User = Depends(get_current_user)):
        db_role = getattr(current_user.role, "value", current_user.role)
        required_value = getattr(required_role, "value", required_role)
        print(f"Current user role from DB: {db_role} | Required role: {required_value}")

        if db_role != required_value:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient privileges")
        return current_user
    return wrapper