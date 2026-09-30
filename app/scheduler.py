import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.models.ticket import Ticket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("helpdesk.scheduler")


async def escalate_old_tickets():
    threshold = datetime.now() - timedelta(hours=24)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Ticket).where(
                Ticket.status == "open",
                Ticket.created_at < threshold,
                Ticket.is_escalated.is_(False),
            )
        )
        tickets = result.scalars().all()

        for ticket in tickets:
            ticket.is_escalated = True

        await db.commit()
        logger.info(f"Escalated {len(tickets)} ticket(s) older than 24h")


async def daily_report():
    async with AsyncSessionLocal() as db:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        open_count = (await db.execute(
            select(func.count(Ticket.id)).where(Ticket.status.in_(["open", "in_progress", "waiting"]))
        )).scalar_one()

        closed_today = (await db.execute(
            select(func.count(Ticket.id)).where(
                Ticket.status == "closed",
                Ticket.updated_at >= today_start,
            )
        )).scalar_one()

        logger.info(f"Daily report — open: {open_count}, closed today: {closed_today}")


scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(escalate_old_tickets, "interval", hours=1, id="escalate_old_tickets")
    scheduler.add_job(daily_report, "cron", hour=0, minute=0, id="daily_report")
    scheduler.start()