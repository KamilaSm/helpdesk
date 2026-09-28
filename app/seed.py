import asyncio
from sqlalchemy import select, update

from app.database import AsyncSessionLocal, engine
from app.models import Plan, Organization

PLANS = [
    {"name": "Free", "ticket_limit": 50, "price": 0},
    {"name": "Pro", "ticket_limit": 200, "price": 1999},
    {"name": "Business", "ticket_limit": -1, "price": 5000},
]


async def seed():
    async with AsyncSessionLocal() as db:
        for data in PLANS:
            result = await db.execute(select(Plan).where(Plan.name == data["name"]))
            if result.scalar_one_or_none() is None:
                db.add(Plan(**data))
        await db.commit()

        free = (await db.execute(select(Plan).where(Plan.name == "Free"))).scalar_one()
        await db.execute(
            update(Organization)
            .where(Organization.plan_id.is_(None))
            .values(plan_id=free.id)
        )
        await db.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())