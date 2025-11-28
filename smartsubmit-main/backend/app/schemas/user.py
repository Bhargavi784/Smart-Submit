from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role:UserRole

    class Config:
        from_attribute = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str