from fastapi import Depends, HTTPException
from starlette import status

from app.models import User
from app.services.user import get_current_user


async def admin_required(current_user: User = Depends(get_current_user)) -> bool:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return True
