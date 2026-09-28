from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.plan import Plan
from app.models.organization import Organization
from app.schemas.billing import UsageOut, PlanChange
from app.dependencies import get_current_user
from app.services.billing import get_plan_and_usage

router = APIRouter()


def build_usage(plan: Plan, used: int) -> UsageOut:
    limit = None if plan.ticket_limit == -1 else plan.ticket_limit
    return UsageOut(plan=plan.name, used=used, limit=limit)


@router.get("/usage", response_model=UsageOut)
async def get_usage(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan, used = await get_plan_and_usage(current_user.org_id, db)
    return build_usage(plan, used)


@router.patch("/plan", response_model=UsageOut)
async def change_plan(
    data: PlanChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change the plan",
        )

    new_plan = (await db.execute(
        select(Plan).where(Plan.id == data.plan_id)
    )).scalar_one_or_none()
    if new_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    org = (await db.execute(
        select(Organization).where(Organization.id == current_user.org_id)
    )).scalar_one()
    org.plan_id = new_plan.id
    await db.commit()

    plan, used = await get_plan_and_usage(current_user.org_id, db)
    return build_usage(plan, used)