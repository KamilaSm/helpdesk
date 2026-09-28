from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.models.organization import Organization
from app.models.plan import Plan


async def get_plan_and_usage(org_id: int, db: AsyncSession) -> tuple[Plan, int]:
    org = (await db.execute(
        select(Organization).where(Organization.id == org_id)
    )).scalar_one()
    plan = (await db.execute(
        select(Plan).where(Plan.id == org.plan_id)
    )).scalar_one()

    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    used = (await db.execute(
        select(func.count(Ticket.id)).where(
            Ticket.org_id == org_id,
            Ticket.created_at >= month_start,
        )
    )).scalar_one()

    return plan, used