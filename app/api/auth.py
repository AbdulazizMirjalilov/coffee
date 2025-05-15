import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_response import BaseResponse, ErrorResponse
from app.core.config import settings
from app.core.db import async_get_db
from app.query.user import create_user_query, get_user_by_email_query
from app.schemas.auth import AuthConfirmResetPassword, AuthLogin
from app.schemas.user import UserCreate
from app.services.auth import auth_token_generate, auth_token_refresh
from app.services.email import render_template, send_email
from app.services.redis import redis_service
from app.services.security import (
    EMAIL_EXPIRE_SECONDS,
    generate_verification_code,
    get_password_hash,
    verify_password,
)
from app.services.user import check_user, get_current_user
from app.tasks import send_email_task

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=BaseResponse)
async def create_user(
    data: UserCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    user = await check_user(db, data.email, data.username)
    if user:
        return BaseResponse(
            success=False,
            message="User with these credentials already exists",
            data=ErrorResponse(name="BadRequest", code=400),
        )

    user_data = data.model_dump()
    verification_code = await generate_verification_code()
    await redis_service.setex(verification_code, EMAIL_EXPIRE_SECONDS, user_data)
    send_email_task.delay(
        {
            "email": data.email,
            "username": data.username,
            "verification_code": verification_code,
        }
    )

    return BaseResponse(
        success=True,
        message="Verification email sent successfully",
        data={"email": data.email},
    )


@router.get("/verify", response_model=BaseResponse)
async def verify_user(
    verification_code: str,
    db: AsyncSession = Depends(async_get_db),
):
    data = await redis_service.get(verification_code)
    if not data:
        return BaseResponse(
            success=False,
            message="Couldn't verify user",
            data=ErrorResponse(name="NotFound", code=404),
        )
    await redis_service.delete(verification_code)
    user_id = await create_user_query(db, data)

    tokens = await auth_token_generate(user_id)
    return BaseResponse(
        success=True,
        message="Verified successfully",
        data={"accessToken": tokens.access_token, "refreshToken": tokens.refresh_token},
    )


@router.post("/login")
async def login(data: AuthLogin, db: AsyncSession = Depends(async_get_db)):
    user = await get_user_by_email_query(db, data.email)
    if user is None:
        return BaseResponse(
            success=False,
            message="Couldn't find user",
            data=ErrorResponse(name="NotFound", code=404),
        )

    is_correct_password = verify_password(user.password, data.password)
    if is_correct_password is False:
        return BaseResponse(
            success=False,
            message="Email or Password is incorrect",
            data=ErrorResponse(name="BadRequest", code=400),
        )

    tokens = await auth_token_generate(user.id)
    return BaseResponse(
        success=True,
        message="Login successfully",
        data={"accessToken": tokens.access_token, "refreshToken": tokens.refresh_token},
    )


@router.get("/reset-password", response_model=BaseResponse)
async def reset_password(email: str, db: AsyncSession = Depends(async_get_db)):
    user = await get_user_by_email_query(db, email)
    if user is None:
        return BaseResponse(
            success=False,
            message="Couldn't find user",
            data=ErrorResponse(name="NotFound", code=404),
        )

    verification_code = await generate_verification_code()
    await redis_service.setex(verification_code, EMAIL_EXPIRE_SECONDS, {"email": email})
    html_content = await render_template(
        "reset_password.html",
        {
            "reset_link": f"{settings.WEB_URL}/password-reset-form?verification_code={verification_code}"  # NOQA
        },
    )
    await send_email(email, user.username, "Reset password", html_content)

    return BaseResponse(
        success=True, message="Email sent to reset password", data={"email": email}
    )


@router.post("/reset-password")
async def confirm_reset_password(
    data: AuthConfirmResetPassword, db: AsyncSession = Depends(async_get_db)
):
    user_data = await redis_service.get(data.token)
    if user_data is None:
        return BaseResponse(
            success=False,
            message="Invalid verification token",
            data=ErrorResponse(name="BadRequest", code=400),
        )
    await redis_service.delete(data.token)
    user = await get_user_by_email_query(db, user_data["email"])
    if user is None:
        return BaseResponse(
            success=False,
            message="Couldn't find user",
            data=ErrorResponse(name="NotFound", code=404),
        )
    user.password = get_password_hash(data.password)
    db.add(user)
    await db.commit()
    return BaseResponse(
        success=True,
        message="Password reset successfully",
        data={"email": user_data["email"]},
    )


@router.post("/refresh-token", response_model=BaseResponse)
async def refresh_token(
    current_user: uuid.UUID = Depends(get_current_user),
):
    token = await auth_token_refresh(current_user)
    return BaseResponse(
        success=True,
        message="Token Generated successfully",
        data={"accessToken": token},
    )
