from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.tickets import TicketCreate, TicketUpdate, TicketOut
from app.dependencies import get_current_user

router = APIRouter()


async def get_ticket_or_404(ticket_id: int, org_id: int, db: AsyncSession) -> Ticket:
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id, Ticket.org_id == org_id)
    )
    ticket = result.scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        org_id=current_user.org_id,
        created_by=current_user.id,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get("", response_model=list[TicketOut])
async def list_tickets(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Ticket).where(Ticket.org_id == current_user.org_id)

    if status_filter is not None:
        query = query.where(Ticket.status == status_filter)
    if priority is not None:
        query = query.where(Ticket.priority == priority)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_ticket_or_404(ticket_id, current_user.org_id, db)


@router.patch("/{ticket_id}", response_model=TicketOut)
async def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ticket = await get_ticket_or_404(ticket_id, current_user.org_id, db)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)

    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete tickets",
        )

    ticket = await get_ticket_or_404(ticket_id, current_user.org_id, db)
    await db.delete(ticket)
    await db.commit()