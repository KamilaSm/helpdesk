from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.schemas.auth import InviteRequest, UserOut
from app.security import hash_password
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/invite", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def invite_user(
    data: InviteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can invite users",
        )

    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role="operator",
        org_id=current_user.org_id,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user