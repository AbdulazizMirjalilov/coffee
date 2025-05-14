from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER


class UserUpdate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    is_verified: bool
    is_active: bool

    class Config:
        from_attributes = True
