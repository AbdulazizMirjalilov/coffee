from pydantic import BaseModel, EmailStr


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str


class AuthLogin(BaseModel):
    email: str
    password: str


class AuthResetPassword(BaseModel):
    email: EmailStr


class AuthConfirmResetPassword(BaseModel):
    token: str
    password: str
