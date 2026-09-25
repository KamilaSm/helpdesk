from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comments import CommentCreate, CommentOut
from app.dependencies import get_current_user
from app.api.tickets import get_ticket_or_404

router = APIRouter()


@router.post("/{ticket_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(
    ticket_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_ticket_or_404(ticket_id, current_user.org_id, db)

    comment = Comment(
        text=data.text,
        ticket_id=ticket_id,
        user_id=current_user.id,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("/{ticket_id}/comments", response_model=list[CommentOut])
async def list_comments(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_ticket_or_404(ticket_id, current_user.org_id, db)

    result = await db.execute(
        select(Comment).where(Comment.ticket_id == ticket_id).order_by(Comment.created_at)
    )
    return result.scalars().all()